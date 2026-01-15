#!/usr/bin/env python3
"""
Fetch word definitions from Free Dictionary API and save as JSON.
Usage: python3 fetch_definitions.py [--input wiki/1-1000.csv] [--output wiki/1-1000-definitions.json]
"""

import json
import time
import urllib.request
import urllib.parse
import urllib.error
import argparse
import os
from pathlib import Path


def fetch_definition(word: str) -> dict | None:
    """Fetch definition for a word from Free Dictionary API."""
    encoded_word = urllib.parse.quote(word)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{encoded_word}"

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and isinstance(data, list):
                entry = data[0]
                return {
                    "word": entry.get("word", word),
                    "phonetic": entry.get("phonetic", ""),
                    "phonetics": entry.get("phonetics", []),
                    "meanings": entry.get("meanings", []),
                    "origin": entry.get("origin", "")
                }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # Word not found
        print(f"  HTTP Error {e.code} for '{word}'")
    except urllib.error.URLError as e:
        print(f"  URL Error for '{word}': {e.reason}")
    except json.JSONDecodeError:
        print(f"  JSON decode error for '{word}'")
    except Exception as e:
        print(f"  Error for '{word}': {e}")

    return None


def load_existing_definitions(output_file: str) -> dict:
    """Load existing definitions from JSON file if it exists."""
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_definitions(definitions: dict, output_file: str):
    """Save definitions to JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(definitions, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Fetch word definitions from Free Dictionary API')
    parser.add_argument('--input', '-i', default='wiki/1-1000.csv', help='Input CSV file with words')
    parser.add_argument('--output', '-o', default=None, help='Output JSON file (default: based on input)')
    parser.add_argument('--delay', '-d', type=float, default=0.5, help='Delay between requests in seconds')
    args = parser.parse_args()

    # Set default output file based on input
    if args.output is None:
        input_stem = Path(args.input).stem
        args.output = f"wiki/{input_stem}-definitions.json"

    # Read words from CSV
    print(f"Reading words from {args.input}...")
    with open(args.input, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    print(f"Found {len(words)} words")

    # Load existing definitions (for resume capability)
    definitions = load_existing_definitions(args.output)
    print(f"Loaded {len(definitions)} existing definitions")

    # Fetch definitions
    success_count = 0
    skip_count = 0
    fail_count = 0
    failed_words = []

    for i, word in enumerate(words, 1):
        # Skip if already fetched
        if word in definitions:
            skip_count += 1
            continue

        print(f"[{i}/{len(words)}] Fetching: {word}", end="", flush=True)

        result = fetch_definition(word)

        if result:
            definitions[word] = result
            success_count += 1
            print(" OK")
        else:
            fail_count += 1
            failed_words.append(word)
            print(" NOT FOUND")

        # Save progress every 50 words
        if i % 50 == 0:
            save_definitions(definitions, args.output)
            print(f"  [Progress saved: {len(definitions)} definitions]")

        # Rate limiting
        time.sleep(args.delay)

    # Final save
    save_definitions(definitions, args.output)

    # Summary
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  Total words: {len(words)}")
    print(f"  Skipped (already fetched): {skip_count}")
    print(f"  Successfully fetched: {success_count}")
    print(f"  Not found: {fail_count}")
    print(f"  Total definitions: {len(definitions)}")
    print(f"  Output file: {args.output}")

    if failed_words:
        print(f"\nWords not found ({len(failed_words)}):")
        for w in failed_words[:20]:
            print(f"  - {w}")
        if len(failed_words) > 20:
            print(f"  ... and {len(failed_words) - 20} more")


if __name__ == "__main__":
    main()
