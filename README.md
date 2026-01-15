# English Words Frequency List

A collection of the most common 10,000 English words and phrases, based on the Wikipedia 2016 corpus from [Wiktionary Frequency Lists](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/English/Wikipedia_(2016)).

## Data Source

The word list is derived from the **Wortschatz Leipzig 2016 English Wikipedia 1M sentence corpus**, provided by Universität Leipzig / Sächsische Akademie der Wissenschaften / InfAI.

Reference:
> D. Goldhahn, T. Eckart & U. Quasthoff. "Building Large Monolingual Dictionaries at the Leipzig Corpora Collection: From 100 to 200 Languages.", in *Proceedings of the 8th International Language Resources and Evaluation (LREC'12)*, 2012.

## File Structure

```
wiki/
├── 1-1000.csv      # Words ranked 1-1000 (most common)
├── 1001-2000.csv   # Words ranked 1001-2000
├── 2001-3000.csv   # Words ranked 2001-3000
├── 3001-4000.csv   # Words ranked 3001-4000
├── 4001-5000.csv   # Words ranked 4001-5000
├── 5001-6000.csv   # Words ranked 5001-6000
├── 6001-7000.csv   # Words ranked 6001-7000
├── 7001-8000.csv   # Words ranked 7001-8000
├── 8001-9000.csv   # Words ranked 8001-9000
└── 9001-10000.csv  # Words ranked 9001-10000
```

## Format

Each CSV file contains one word or phrase per line, ordered by frequency rank. The list includes:

- Single words: `the`, `of`, `and`, `to`, `in`
- Common phrases: `such as`, `as well as`, `in order to`, `United States`
- Abbreviations: `p.`, `e.g.`, `i.e.`

### Example (1-1000.csv)

```
the
of
and
to
in
a
is
was
...
on the
such as
```

## Statistics

| File | Word Count |
|------|------------|
| 1-1000.csv | 1,000 |
| 1001-2000.csv | 999 |
| 2001-3000.csv | 996 |
| 3001-4000.csv | 999 |
| 4001-5000.csv | 992 |
| 5001-6000.csv | 994 |
| 6001-7000.csv | 995 |
| 7001-8000.csv | 990 |
| 8001-9000.csv | 990 |
| 9001-10000.csv | 986 |
| **Total** | **9,941** |

## Usage

These word lists can be used for:

- Language learning and vocabulary building
- Text analysis and natural language processing
- Spell checking and autocomplete systems
- Reading level assessment
- Corpus linguistics research

## License

The original data is available under the [Creative Commons Attribution-ShareAlike License](https://creativecommons.org/licenses/by-sa/4.0/).
