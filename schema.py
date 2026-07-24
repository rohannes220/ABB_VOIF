"""
Common row schema every scraper writes into, plus a shared CSV writer.

This mirrors the columns already in ABB_Data_Cleaned.xlsx (brand, platform,
type, product name, rating, city, text) so scraper output drops straight
into the existing pipeline. `sentiment` and `intent` are intentionally left
blank here — those are filled in a later NLP labeling step, not by the
scraper.
"""
import csv
import hashlib
import os
from dataclasses import dataclass, fields, asdict
from datetime import datetime, timezone
from typing import Optional

OUTPUT_COLUMNS = [
    "brand",
    "platform",
    "type",
    "product_name",
    "rating",
    "city",
    "text",
    "sentiment",
    "intent",
    "source_url",
    "review_date",
    "scraped_at",
    "row_hash",
]


@dataclass
class Review:
    brand: str
    platform: str
    text: str
    type: str = ""              # driver/topic: Store Experience, Product Quality, etc.
    product_name: str = ""
    rating: Optional[float] = None
    city: str = ""
    sentiment: str = ""         # filled later by NLP step
    intent: str = ""            # filled later by NLP step
    source_url: str = ""
    review_date: str = ""

    def row_hash(self) -> str:
        """Stable hash for de-duplication across scraper runs."""
        key = f"{self.brand}|{self.platform}|{self.text.strip().lower()}"
        return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]

    def to_row(self) -> dict:
        d = asdict(self)
        d["scraped_at"] = datetime.now(timezone.utc).isoformat()
        d["row_hash"] = self.row_hash()
        return d


def write_reviews(reviews: list, output_path: str, append: bool = True) -> int:
    """
    Write Review objects to CSV, de-duplicating against any rows already in
    the file (by row_hash). Returns the number of NEW rows written.
    """
    existing_hashes = set()
    file_exists = os.path.isfile(output_path)

    if append and file_exists:
        with open(output_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_hashes.add(row.get("row_hash", ""))

    new_rows = []
    for r in reviews:
        row = r.to_row()
        if row["row_hash"] in existing_hashes:
            continue
        existing_hashes.add(row["row_hash"])
        new_rows.append(row)

    mode = "a" if (append and file_exists) else "w"
    write_header = not (append and file_exists)

    with open(output_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        if write_header:
            writer.writeheader()
        for row in new_rows:
            writer.writerow(row)

    return len(new_rows)
