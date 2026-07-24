"""
MouthShut scraper — best-effort, no login/API key.

APPROACH HISTORY:
1. requests + BeautifulSoup against the static page HTML. Consistently
   found "no review cards" for every brand — turned out the page's raw
   HTML only contains the vote count and a "Reviews" tab link; individual
   review text is injected by JavaScript after the page loads, not present
   in the static HTML at all.
2. CURRENT: switched to Playwright (real browser), same approach as the
   Google Reviews scraper — load the page, let the JS render, then read
   the review text out of the DOM. Unlike Myntra, MouthShut doesn't appear
   to have aggressive bot-detection, so this should work without the
   fresh-context-per-request workaround Myntra needed.
"""
import os
import time
from playwright.sync_api import sync_playwright

from config import MOUTHSHUT_BRAND_URLS, REQUEST_DELAY_SECONDS
from schema import Review

HEADLESS = os.environ.get("MOUTHSHUT_HEADLESS", "true").lower() != "false"


def scrape_brand(page, brand: str, max_scrolls: int = 15) -> list[Review]:
    base_url = MOUTHSHUT_BRAND_URLS.get(brand, "")
    if not base_url:
        print(f"[MouthShut] No URL configured for '{brand}' in config.py — skipping.")
        return []

    page.goto(base_url, timeout=30000)
    time.sleep(2)

    try:
        page.click("a[href='#dvreview-listing']", timeout=5000)
    except Exception:
        pass
    time.sleep(1.5)

    for _ in range(max_scrolls):
        page.mouse.wheel(0, 2500)
        time.sleep(0.8)

    cards = page.query_selector_all(
        "div.reviewdata, div[itemprop='review'], div.row.reviewrow"
    )

    if not cards:
        try:
            page.screenshot(path=f"debug_mouthshut_{brand.replace(' ', '_')}.png", full_page=True)
            print(f"[MouthShut]   DEBUG: no review cards found for '{brand}', "
                  f"saved debug_mouthshut_{brand.replace(' ', '_')}.png")
        except Exception:
            pass
        return []

    results = []
    for card in cards:
        text_el = card.query_selector("p, div.more, span[itemprop='reviewBody']")
        text = text_el.inner_text().strip() if text_el else card.inner_text().strip()
        if not text:
            continue

        rating = None
        rating_el = card.query_selector("[title*='Rating'], meta[itemprop='ratingValue']")
        if rating_el:
            raw = rating_el.get_attribute("title") or rating_el.get_attribute("content") or ""
            digits = "".join(c for c in raw if c.isdigit() or c == ".")
            try:
                rating = float(digits) if digits else None
            except ValueError:
                rating = None

        results.append(Review(
            brand=brand,
            platform="MouthShut",
            text=text,
            rating=rating,
            source_url=base_url,
        ))

    return results


def scrape_all(brands: list) -> list[Review]:
    all_reviews = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        for brand in brands:
            try:
                reviews = scrape_brand(page, brand)
                all_reviews.extend(reviews)
                print(f"[MouthShut] {brand}: {len(reviews)} reviews")
            except Exception as e:
                print(f"[MouthShut] Failed on '{brand}': {e}")
            time.sleep(REQUEST_DELAY_SECONDS)

        browser.close()

    return all_reviews