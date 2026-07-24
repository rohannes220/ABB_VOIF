"""
Reviews.io scraper — best-effort HTML scraping (no API key required).

Reviews.io company pages are server-rendered and paginate with a simple
?page= query param, which makes this the most reliable scraper in this
project after MouthShut. Still fragile to markup changes — see 'SELECTOR:'
comments if it starts returning nothing.
"""
import time
import requests
from bs4 import BeautifulSoup

from config import REVIEWSIO_BRAND_URLS, REQUEST_TIMEOUT, REQUEST_DELAY_SECONDS, USER_AGENT
from schema import Review

HEADERS = {"User-Agent": USER_AGENT}


def _parse_review_card(card, brand: str, url: str) -> Review | None:
    # SELECTOR: review body text
    text_el = card.select_one("[data-testid='review-content'], .review-content p, p.review-body")
    text = text_el.get_text(strip=True) if text_el else ""
    if not text:
        return None

    # SELECTOR: star rating, usually in an aria-label like "Rated 5 out of 5"
    rating = None
    star_el = card.select_one("[aria-label*='out of 5'], .star-rating")
    if star_el and star_el.has_attr("aria-label"):
        label = star_el["aria-label"]
        digits = "".join(c for c in label.split("out")[0] if c.isdigit() or c == ".")
        try:
            rating = float(digits) if digits else None
        except ValueError:
            rating = None

    # SELECTOR: reviewer-stated date
    date_el = card.select_one("time, .review-date")
    review_date = date_el.get("datetime", date_el.get_text(strip=True)) if date_el else ""

    return Review(
        brand=brand,
        platform="Reviews.io",
        text=text,
        rating=rating,
        source_url=url,
        review_date=review_date,
    )


def scrape_brand(brand: str, max_pages: int = 5) -> list[Review]:
    base_url = REVIEWSIO_BRAND_URLS.get(brand, "")
    if not base_url:
        print(f"[Reviews.io] No URL configured for '{brand}' in config.py — skipping.")
        return []

    results = []
    for page in range(1, max_pages + 1):
        sep = "&" if "?" in base_url else "?"
        page_url = base_url if page == 1 else f"{base_url}{sep}page={page}"
        try:
            resp = requests.get(page_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"[Reviews.io] Failed to fetch {page_url}: {e}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        # SELECTOR: review card container
        cards = soup.select("[data-testid='review-card'], .review-card, article.review")
        if not cards:
            print(f"[Reviews.io] No review cards found on page {page} — "
                  f"selectors likely need updating, or this is the last page.")
            break

        for card in cards:
            review = _parse_review_card(card, brand, page_url)
            if review:
                results.append(review)

        time.sleep(REQUEST_DELAY_SECONDS)

    return results


def scrape_all(brands: list) -> list[Review]:
    all_reviews = []
    for brand in brands:
        all_reviews.extend(scrape_brand(brand))
    return all_reviews
