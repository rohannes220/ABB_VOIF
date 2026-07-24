"""
Orchestrator — run one platform or all of them, writing combined output
into a single CSV that matches the existing ABB_Data_Cleaned.xlsx schema.

Usage:
    python main.py --platform mouthshut
    python main.py --platform reviewsio
    python main.py --platform myntra
    python main.py --platform google
    python main.py --platform twitter
    python main.py --platform instagram
    python main.py --platform all
"""
import argparse
import sys

from config import BRANDS
from schema import write_reviews

PLATFORM_MODULES = {
    "mouthshut": "scrapers.mouthshut",
    "reviewsio": "scrapers.reviewsio",
    "google": "scrapers.google_reviews",
}


def run_platform(name: str, output_path: str):
    import importlib
    module = importlib.import_module(PLATFORM_MODULES[name])
    print(f"\n=== Running {name} scraper for brands: {', '.join(BRANDS)} ===")
    reviews = module.scrape_all(BRANDS)
    new_count = write_reviews(reviews, output_path, append=True)
    print(f"=== {name}: {len(reviews)} scraped, {new_count} new rows written to {output_path} ===")


def main():
    parser = argparse.ArgumentParser(description="VoC-Fashion scraper orchestrator")
    parser.add_argument(
        "--platform",
        choices=list(PLATFORM_MODULES.keys()) + ["all"],
        default="all",
        help="Which platform to scrape (default: all)",
    )
    parser.add_argument(
        "--output",
        default="voc_fashion_raw.csv",
        help="Output CSV path (default: voc_fashion_raw.csv)",
    )
    args = parser.parse_args()

    platforms = list(PLATFORM_MODULES.keys()) if args.platform == "all" else [args.platform]

    for platform in platforms:
        try:
            run_platform(platform, args.output)
        except Exception as e:
            print(f"[main] {platform} scraper crashed: {e}", file=sys.stderr)
            continue


if __name__ == "__main__":
    main()
