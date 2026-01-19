#!/usr/bin/env python3
"""
Convert wiki CSV files to JSON format for the English Words app.

Input: wiki/*.csv (one word per line)
Output: public/data/group-{range}.json

JSON format:
[
  { "rank": 1, "word": "the" },
  { "rank": 2, "word": "of" },
  ...
]
"""

import json
import os
from pathlib import Path

# Define paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
WIKI_DIR = PROJECT_ROOT / "wiki"
OUTPUT_DIR = PROJECT_ROOT / "public" / "data"

# CSV files to process (in order)
CSV_FILES = [
    ("1-1000.csv", "1-1000", 1),
    ("1001-2000.csv", "1001-2000", 1001),
    ("2001-3000.csv", "2001-3000", 2001),
    ("3001-4000.csv", "3001-4000", 3001),
    ("4001-5000.csv", "4001-5000", 4001),
    ("5001-6000.csv", "5001-6000", 5001),
    ("6001-7000.csv", "6001-7000", 6001),
    ("7001-8000.csv", "7001-8000", 7001),
    ("8001-9000.csv", "8001-9000", 8001),
    ("9001-10000.csv", "9001-10000", 9001),
]


def read_csv(file_path: Path) -> list[str]:
    """Read CSV file and return list of words."""
    words = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word:  # Skip empty lines
                words.append(word)
    return words


def convert_to_json(words: list[str], start_rank: int) -> list[dict]:
    """Convert word list to JSON format with ranks."""
    return [
        {"rank": start_rank + i, "word": word}
        for i, word in enumerate(words)
    ]


def main():
    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total_words = 0

    for csv_filename, group_name, start_rank in CSV_FILES:
        csv_path = WIKI_DIR / csv_filename

        if not csv_path.exists():
            print(f"⚠️  Skipping {csv_filename} (file not found)")
            continue

        # Read and convert
        words = read_csv(csv_path)
        json_data = convert_to_json(words, start_rank)

        # Write JSON file
        output_filename = f"group-{group_name}.json"
        output_path = OUTPUT_DIR / output_filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        total_words += len(words)
        print(f"✅ {csv_filename} -> {output_filename} ({len(words)} words)")

    print(f"\n🎉 Done! Total: {total_words} words converted")
    print(f"📁 Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
