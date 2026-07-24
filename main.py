"""
Orchestrator — run one platform or all of them, writing combined output
into a single CSV that matches the existing ABB_Data_Cleaned.xlsx schema.
"""

import argparse
import sys
from datetime import datetime

from config import BRANDS
from schema import write_reviews

PLATFORM_MODULES = {
    "mouthshut": "scrapers.mouthshut",
    "google": "scrapers.google_reviews",
}


def run_platform(name: str, output_path: str, append: bool):
    import importlib

    module = importlib.import_module(PLATFORM_MODULES[name])

    print(f"\n=== Running {name} scraper for brands: {', '.join(BRANDS)} ===")

    reviews = module.scrape_all(BRANDS)

    new_count = write_reviews(reviews, output_path, append=append)

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
        default=None,
        help="Optional output CSV path",
    )

    args = parser.parse_args()

    if args.output is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        args.output = f"output/voc_fashion_raw_{timestamp}.csv"

    platforms = list(PLATFORM_MODULES.keys()) if args.platform == "all" else [args.platform]

    first = True

    for platform in platforms:
        try:
            run_platform(
                platform,
                args.output,
                append=not first,
            )
            first = False

        except Exception as e:
            print(f"[main] {platform} scraper crashed: {e}", file=sys.stderr)
            continue


if __name__ == "__main__":
    main()