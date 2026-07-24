"""
Google Reviews scraper — best-effort, no Places API key.

Google Maps renders reviews client-side and lazy-loads them on scroll, so
this needs a real (headless) browser rather than requests+BeautifulSoup.
Uses Playwright, which is free/open-source (unlike the Places API, which
bills per request). This is the most fragile scraper in the project:
Google changes Maps' DOM structure periodically and can rate-limit or
CAPTCHA-block an IP that scrapes too fast — keep REQUEST_DELAY_SECONDS
generous and don't run this in a tight loop.

One-time setup:
    pip install playwright
    playwright install chromium
"""
import os
import time
from playwright.sync_api import sync_playwright

from config import BRANDS, CITIES, REQUEST_DELAY_SECONDS
from schema import Review

# Set GOOGLE_HEADLESS=false in your terminal to watch the browser live
# instead of running invisibly — very useful for debugging "0 stores found".
# Example:  GOOGLE_HEADLESS=false python main.py --platform google
HEADLESS = os.environ.get("GOOGLE_HEADLESS", "true").lower() != "false"


def _scroll_reviews_panel(page, pause_s: float = 1.5, max_scrolls: int = 20):
    """Google Maps loads more reviews as you scroll the reviews panel."""
    panel_selector = 'div[aria-label*="Reviews"]'
    try:
        page.wait_for_selector(panel_selector, timeout=8000)
    except Exception:
        return  # panel never appeared — likely no results for this query

    for _ in range(max_scrolls):
        page.mouse.wheel(0, 3000)
        time.sleep(pause_s)


def _find_store_results(page, query: str, max_stores: int = 8) -> list[dict]:
    """
    Run a Maps search for '<brand> store <city>' and collect every store
    result Google returns (name + link), instead of just the first one.
    If the search lands directly on a single place (no list), returns that
    one store.
    """
    search_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
    page.goto(search_url, timeout=30000)
    time.sleep(2)

    # Dismiss Google's cookie/consent screen if it appears — this blocks
    # everything else on the page until clicked, and is the #1 cause of
    # "found 0 stores" in headless mode.
    for consent_text in ["Accept all", "I agree", "Accept", "Reject all"]:
        try:
            page.click(f"button:has-text('{consent_text}')", timeout=3000)
            time.sleep(1.5)
            break
        except Exception:
            continue

    # SELECTOR: result cards in the left-hand list panel. Each has an <a>
    # with the place name as its accessible/aria-label text.
    anchors = page.query_selector_all("a.hfpxzc")

    if not anchors:
        # No list panel found. Save a screenshot + the raw page text so we
        # can see exactly what the browser was looking at instead of
        # guessing — check debug_<query>.png after a run that finds 0 stores.
        safe_name = "".join(c if c.isalnum() else "_" for c in query)[:60]
        try:
            page.screenshot(path=f"debug_{safe_name}.png", full_page=True)
            print(f"[Google Reviews]   DEBUG: no store list found, saved debug_{safe_name}.png")
        except Exception:
            pass
        # Fall back to treating this as a single-place page, but only if it
        # actually looks like one (has a reviews-related element somewhere).
        return [{"name": query, "url": page.url}]

    stores = []
    for a in anchors[:max_stores]:
        name = a.get_attribute("aria-label") or query
        href = a.get_attribute("href")
        if href:
            stores.append({"name": name, "url": href})

    return stores


def scrape_store(page, store: dict, brand: str, city: str) -> list[Review]:
    """Scrape all reviews for one specific store page (already-known URL)."""
    page.goto(store["url"], timeout=30000)
    time.sleep(2)

    # Click the "Reviews" tab. SELECTOR: tab button text match.
    try:
        page.click("button:has-text('Reviews')", timeout=5000)
        time.sleep(2)
    except Exception:
        print(f"[Google Reviews] Could not find Reviews tab for '{store['name']}' — skipping.")
        return []

    _scroll_reviews_panel(page)

    # SELECTOR: individual review card container. Google's class names are
    # obfuscated/auto-generated and DO change — if this returns nothing,
    # re-inspect via browser devtools and update.
    cards = page.query_selector_all("div[data-review-id]")

    results = []
    for card in cards:
        text_el = card.query_selector("span.wiI7pd")
        text = text_el.inner_text().strip() if text_el else ""
        if not text:
            continue

        rating = None
        rating_el = card.query_selector("span[role='img']")
        if rating_el:
            label = rating_el.get_attribute("aria-label") or ""
            digits = "".join(c for c in label if c.isdigit() or c == ".")
            try:
                rating = float(digits) if digits else None
            except ValueError:
                rating = None

        results.append(Review(
            brand=brand,
            platform="Google",
            type="Store Experience",
            text=text,
            rating=rating,
            city=f"{store['name']} — {city}",
            source_url=store["url"],
        ))

    return results


def scrape_query(page, query: str, brand: str, city: str, max_stores: int = 8) -> list[Review]:
    """Find every store for this brand+city search, then scrape each one's reviews."""
    stores = _find_store_results(page, query, max_stores=max_stores)
    all_results = []
    for store in stores:
        try:
            reviews = scrape_store(page, store, brand, city)
            all_results.extend(reviews)
            print(f"[Google Reviews]   {store['name']}: {len(reviews)} reviews")
        except Exception as e:
            print(f"[Google Reviews]   Failed on store '{store['name']}': {e}")
        time.sleep(1.5)
    return all_results


def scrape_all(brands: list = None, cities: list = None) -> list[Review]:
    brands = brands or BRANDS
    cities = cities or CITIES

    all_reviews = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
            ],
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            viewport={"width": 1366, "height": 768},
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Upgrade-Insecure-Requests": "1",
            },
        )

        page = context.new_page()

        for brand in brands:
            for city in cities:
                query = f"{brand} store {city}"
                try:
                    reviews = scrape_query(page, query, brand, city)
                    all_reviews.extend(reviews)
                    print(
                        f"[Google Reviews] {query}: "
                        f"{len(reviews)} total reviews across all stores found"
                    )
                except Exception as e:
                    print(f"[Google Reviews] Failed on '{query}': {e}")

                time.sleep(REQUEST_DELAY_SECONDS)

        context.close()
        browser.close()

    return all_reviews