"""
Central configuration for the VoC-Fashion scraper.
Edit this file to add/remove brands, cities, or seed URLs — nothing else
in the codebase should need brand names hardcoded.
"""

# Brands confirmed from ABB_Data_Cleaned sample
BRANDS = [
    "Allen Solly",
    "Louis Philippe",
    "Van Heusen",
    "Peter England",
    "American Eagle",
    "Reebok",
]

# Cities/stores seen in the cleaned sample — used to build Google Maps
# search queries ("<brand> store <city>"). Add/remove as needed.
CITIES = [
    "Bangalore",
    "Mumbai",
    "Delhi",
    "Chennai",
    "Kolkata",
    "Hyderabad",
    "Pune",
    "Ahmedabad",
]

# MouthShut and Reviews.io use brand-slug URLs. Fill these in once you've
# located the correct slug for each brand on each site (search the site,
# copy the brand page URL). Left blank = skipped by that scraper.
MOUTHSHUT_BRAND_URLS = {
    "Allen Solly": "https://www.mouthshut.com/product-reviews/allen-solly-reviews-925004840",
    "Louis Philippe": "https://www.mouthshut.com/product-reviews/louis-philippe-reviews-925008952",
    "Van Heusen": "https://www.mouthshut.com/product-reviews/van-heusen-reviews-925004842",
    "Peter England": "https://www.mouthshut.com/product-reviews/peter-england-reviews-925004847",
    "American Eagle": "",
    "Reebok": "https://www.mouthshut.com/product-reviews/reebok-reviews-926171869",
}


# Twitter/X search handles or hashtags per brand (used by the snscrape-based
# scraper). No login required, but X actively blocks this — expect breakage.

# Instagram hashtags/handles per brand (used by instaloader). Instagram
# requires a logged-in session for anything beyond a handful of posts.
INSTAGRAM_HASHTAGS = {
    "Allen Solly": "allensolly",
    "Louis Philippe": "louisphilippe",
    "Van Heusen": "vanheusen",
    "Peter England": "peterengland",
    "American Eagle": "americaneagleindia",
    "Reebok": "reebokindia",
}

REQUEST_TIMEOUT = 15
REQUEST_DELAY_SECONDS = 2.5  # politeness delay between requests
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
