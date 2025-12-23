# Chronological Sorting Demonstration

This file demonstrates how podcast episode files are named and sorted chronologically.

## How Files Are Named

The podcast downloader creates MP3 files with this naming pattern:
```
YYYY-MM-DD_Title.mp3
```

Where:
- `YYYY` = 4-digit year
- `MM` = 2-digit month
- `DD` = 2-digit day
- `Title` = Episode title (cleaned and sanitized)

## Example Files

Here are example filenames that would be created by the downloader:

```
2025-12-18_La_crème_de_la_crème__‐_Jour_19.mp3
2025-12-19_Ça_sent_le_sapin_pour_les_sapins__‐_Jour_20.mp3
2025-12-20_La_petite_flamme_du_cœur__‐_Jour_21.mp3
2025-12-21_Sous_le_feu_des_projecteurs__‐_Jour_22.mp3
2025-12-22_Esprit_de_Noël_es_tu_là__‐_Jour_23.mp3
2025-12-23_Le_dernier_jour_avant_Noël__‐_Jour_24.mp3
```

## Chronological Sorting

When you list these files with `ls`, they will automatically appear in chronological order:

```bash
$ ls
2025-12-18_La_crème_de_la_crème__‐_Jour_19.mp3
2025-12-19_Ça_sent_le_sapin_pour_les_sapins__‐_Jour_20.mp3
2025-12-20_La_petite_flamme_du_cœur__‐_Jour_21.mp3
2025-12-21_Sous_le_feu_des_projecteurs__‐_Jour_22.mp3
2025-12-22_Esprit_de_Noël_es_tu_là__‐_Jour_23.mp3
2025-12-23_Le_dernier_jour_avant_Noël__‐_Jour_24.mp3
```

This is because the ISO 8601 date format (YYYY-MM-DD) sorts alphabetically in chronological order.

## Why This Works

The ISO 8601 format ensures chronological sorting because:

1. **Year first**: 2025 comes before 2026
2. **Month second**: December (12) comes before January (01) of the next year
3. **Day third**: Day 20 comes before day 21

Example comparison:
- `2025-12-20` < `2025-12-21` (December 20 < December 21)
- `2025-12-31` < `2026-01-01` (Dec 31, 2025 < Jan 1, 2026)

## Real-World Example

From the RTS podcast example in USAGE_EXAMPLE.md:

```
Les_histoires_de_Millie_D._‐_RTS/
├── 2025-12-22_Esprit_de_Noël_es_tu_là__‐_Jour_23.mp3
├── 2025-12-21_Sous_le_feu_des_projecteurs__‐_Jour_22.mp3
├── 2025-12-20_La_petite_flamme_du_cœur__‐_Jour_21.mp3
├── 2025-12-19_Ça_sent_le_sapin_pour_les_sapins__‐_Jour_20.mp3
├── 2025-12-18_La_crème_de_la_crème__‐_Jour_19.mp3
└── README.md
```

When sorted alphabetically, these files appear in reverse chronological order (newest first).
To see them in chronological order (oldest first), use:

```bash
ls -r
```

Or to see them in chronological order (oldest first):

```bash
ls | sort -r
```

## Benefits of This Approach

1. **Natural sorting**: No need for special tools or scripts
2. **Human-readable**: Dates are easy to understand
3. **Consistent**: Works across all operating systems
4. **Standard**: Follows ISO 8601 international standard
5. **Searchable**: Easy to find episodes by date

## Creating Your Own Test Files

You can create test files to verify the sorting:

```bash
# Create test files with dates
touch 2025-01-15_Test_Episode_1.mp3
touch 2025-02-20_Test_Episode_2.mp3
touch 2025-03-10_Test_Episode_3.mp3

# List them (they'll be in chronological order)
ls
```

## Troubleshooting

If files don't sort correctly:

1. **Check the format**: Ensure dates are in YYYY-MM-DD format
2. **Check for leading zeros**: Month and day must be 2 digits (01-12, 01-31)
3. **Check for extra characters**: No spaces or special characters before the date
4. **Use `sort -V`**: For version sorting (handles multi-digit numbers)

```bash
ls | sort -V
```
