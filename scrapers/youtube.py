"""
YouTube comments collector using the official YouTube Data API v3.

The scraper searches YouTube for recent/relevant videos mentioning each
configured brand, then collects top-level public comments and converts them
into the shared Review schema used by the rest of the VoC pipeline.

Setup:
    1. Create a YouTube Data API v3 key in Google Cloud Console.
    2. Export it before running:
           export YOUTUBE_API_KEY="your_key_here"
    3. Run:
           python3 main.py --platform youtube

Optional environment variables:
    YOUTUBE_MAX_VIDEOS_PER_BRAND   default: 5
    YOUTUBE_MAX_COMMENTS_PER_VIDEO default: 100

Notes:
- This uses the supported API rather than browser automation.
- Some videos have comments disabled; those videos are skipped.
- `rating` and `city` are blank because YouTube comments do not provide them.
"""

import html
import os
import re
import time
from typing import Optional

import requests

from config import BRANDS, REQUEST_DELAY_SECONDS, YOUTUBE_SEARCH_QUERIES
from schema import Review

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"
MAX_VIDEOS_PER_BRAND = int(os.environ.get("YOUTUBE_MAX_VIDEOS_PER_BRAND", "5"))
MAX_COMMENTS_PER_VIDEO = int(os.environ.get("YOUTUBE_MAX_COMMENTS_PER_VIDEO", "100"))


def _api_key() -> str:
    key = os.environ.get("YOUTUBE_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "YOUTUBE_API_KEY is not set. Export a YouTube Data API v3 key first: "
            'export YOUTUBE_API_KEY="your_key_here"'
        )
    return key


def _clean_comment(text: str) -> str:
    """Convert YouTube's HTML-ish display text into plain normalized text."""
    text = html.unescape(text or "")
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return " ".join(text.split()).strip()


def _get_json(endpoint: str, params: dict) -> dict:
    params = dict(params)
    params["key"] = _api_key()
    response = requests.get(
        f"{YOUTUBE_API_BASE}/{endpoint}",
        params=params,
        timeout=20,
    )

    if response.status_code == 403:
        detail = ""
        try:
            detail = response.json().get("error", {}).get("message", "")
        except Exception:
            pass
        raise RuntimeError(f"YouTube API returned 403. {detail}".strip())

    response.raise_for_status()
    return response.json()


def search_videos(query: str, max_results: int = MAX_VIDEOS_PER_BRAND) -> list[dict]:
    """Search YouTube and return video id/title/url records."""
    if max_results <= 0:
        return []

    data = _get_json(
        "search",
        {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": min(max_results, 50),
            "order": "relevance",
            "safeSearch": "moderate",
        },
    )

    videos = []
    for item in data.get("items", []):
        video_id = item.get("id", {}).get("videoId")
        snippet = item.get("snippet", {})
        if not video_id:
            continue
        videos.append(
            {
                "video_id": video_id,
                "title": html.unescape(snippet.get("title", "")).strip(),
                "channel_title": html.unescape(snippet.get("channelTitle", "")).strip(),
                "published_at": snippet.get("publishedAt", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}",
            }
        )
    return videos


def get_video_comments(
    video: dict,
    brand: str,
    max_comments: int = MAX_COMMENTS_PER_VIDEO,
) -> list[Review]:
    """Collect top-level public comments for a single YouTube video."""
    if max_comments <= 0:
        return []

    results = []
    page_token: Optional[str] = None

    while len(results) < max_comments:
        params = {
            "part": "snippet",
            "videoId": video["video_id"],
            "maxResults": min(100, max_comments - len(results)),
            "textFormat": "html",
            "order": "relevance",
        }
        if page_token:
            params["pageToken"] = page_token

        try:
            data = _get_json("commentThreads", params)
        except requests.HTTPError as exc:
            # Comments-disabled videos normally return 403. If Google changes
            # the error code, skip the video rather than crashing the whole run.
            print(f"[YouTube]   Could not read comments for '{video['title']}': {exc}")
            return results
        except RuntimeError as exc:
            # A 403 can mean comments disabled OR an API/quota/auth issue.
            message = str(exc).lower()
            if "commentsdisabled" in message or "disabled comments" in message:
                print(f"[YouTube]   Comments disabled for '{video['title']}' — skipping.")
                return results
            raise

        for item in data.get("items", []):
            snippet = (
                item.get("snippet", {})
                .get("topLevelComment", {})
                .get("snippet", {})
            )
            text = _clean_comment(snippet.get("textDisplay", ""))
            if not text:
                continue

            results.append(
                Review(
                    brand=brand,
                    platform="YouTube",
                    type="Social / Video Feedback",
                    product_name=video.get("title", ""),
                    text=text,
                    rating=None,
                    city="",
                    source_url=video.get("url", ""),
                    review_date=snippet.get("publishedAt", ""),
                )
            )

            if len(results) >= max_comments:
                break

        page_token = data.get("nextPageToken")
        if not page_token:
            break

        time.sleep(min(REQUEST_DELAY_SECONDS, 1.0))

    return results


def scrape_brand(brand: str) -> list[Review]:
    query = YOUTUBE_SEARCH_QUERIES.get(brand) or f"{brand} review India fashion"
    videos = search_videos(query, MAX_VIDEOS_PER_BRAND)

    print(f"[YouTube] {brand}: found {len(videos)} videos for query '{query}'")

    reviews = []
    for video in videos:
        try:
            comments = get_video_comments(video, brand, MAX_COMMENTS_PER_VIDEO)
            reviews.extend(comments)
            print(f"[YouTube]   {video['title'][:70]}: {len(comments)} comments")
        except Exception as exc:
            print(f"[YouTube]   Failed on video '{video['title']}': {exc}")
        time.sleep(REQUEST_DELAY_SECONDS)

    return reviews


def scrape_all(brands: list = None) -> list[Review]:
    brands = brands or BRANDS
    all_reviews = []

    # Fail immediately with a useful message instead of running brand loops
    # when credentials are missing.
    _api_key()

    for brand in brands:
        try:
            reviews = scrape_brand(brand)
            all_reviews.extend(reviews)
            print(f"[YouTube] {brand}: {len(reviews)} total comments")
        except Exception as exc:
            print(f"[YouTube] Failed on '{brand}': {exc}")
        time.sleep(REQUEST_DELAY_SECONDS)

    return all_reviews
