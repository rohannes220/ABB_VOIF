# VoC-Fashion Scraper

Best-effort HTML/open-source scraper for the six brands in scope
(Allen Solly, Louis Philippe, Van Heusen, Peter England, American Eagle,
Reebok) across the six platforms already represented in
`ABB_Data_Cleaned.xlsx` (Google, Myntra, Twitter, MouthShut, Reviews.io,
Instagram). No paid APIs are used — see the caveats below for what that
trade-off costs you per platform.

## Setup

```bash
pip install -r requirements.txt
playwright install chromium   # only needed for the Google Reviews scraper
```

## Running

```bash
python main.py --platform mouthshut     # or reviewsio / myntra / google / twitter / instagram / all
```

Output appends to `voc_fashion_raw.csv` (or whatever you pass to `--output`),
de-duplicated by a hash of brand+platform+text so re-running a scraper
doesn't create duplicate rows.

## Before you run anything

Open `config.py` and fill in the blanks:

- `MOUTHSHUT_BRAND_URLS` / `REVIEWSIO_BRAND_URLS` — find each brand's page on
  the site and paste the URL in. Left blank, that brand is skipped.
- `MYNTRA_PRODUCT_IDS` — Myntra has no brand-level review page, only
  per-product reviews, so you need to seed a handful of product IDs per
  brand (the numeric ID in the product URL).
- `CITIES` — already pre-filled from your cleaned sample; adjust if the
  final store list changes.

## Platform-by-platform reliability (read this before you trust the output)

| Platform | Method | Reliability | Notes |
|---|---|---|---|
| **MouthShut** | requests + BeautifulSoup | Highest | Server-rendered HTML, no browser needed |
| **Reviews.io** | requests + BeautifulSoup | High | Server-rendered, simple pagination |
| **Myntra** | requests to internal JSON endpoint | Medium | Endpoint isn't officially public — can change without notice; needs product IDs seeded manually |
| **Google Reviews** | Playwright (headless browser) | Medium-Low | JS-heavy, obfuscated class names that change periodically, Google may rate-limit/CAPTCHA a fast-scraping IP |
| **Twitter/X** | snscrape | Low | X has aggressively blocked unauthenticated scraping since 2023; this may simply stop returning results at any time |
| **Instagram** | instaloader | Low (small volume only) | Anonymous requests are rate-limited hard; realistically good for ~20-30 posts/comments per run, not bulk collection |

**Practical implication for your project:** MouthShut, Reviews.io, and
Myntra are the platforms you can actually build volume on. Google Reviews
will work but needs babysitting (expect to fix a selector every so often).
Twitter and Instagram should be treated as thin supplementary evidence —
don't plan your sentiment/intent analysis around having deep coverage there,
since the scraping methods available without a paid API are structurally
limited on both.

If bulk Twitter/Instagram volume turns out to matter for the deliverables,
that's worth flagging to Sri/your client contact as a case for a paid API
budget, rather than something to force through fragile scraping.

## Output schema

All scrapers write into the same row shape (see `schema.py`):

```
brand, platform, type, product_name, rating, city, text, sentiment, intent,
source_url, review_date, scraped_at, row_hash
```

`sentiment` and `intent` are left blank by design — those get filled in a
separate NLP labeling step downstream, matching how `ABB_Data_Cleaned.xlsx`
already separates raw text from its labels.

## Selector maintenance

Every scraper that parses HTML has `SELECTOR:` comments marking the CSS
selectors most likely to break when a site updates its markup. If a
scraper suddenly returns zero results, that's the first thing to check —
open the page in a browser, inspect the relevant element, and update the
selector in that file.
