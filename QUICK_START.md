# Quick Start Guide

## 1. Install Dependencies

```bash
pip install feedparser requests
```

## 2. Run the Downloader

```bash
python3 podcast_downloader.py https://example.com/podcast.rss
```

## 3. Customize (Optional)

Download 20 episodes to a specific folder:

```bash
python3 podcast_downloader.py https://example.com/podcast.rss -n 20 -o ~/podcasts
```

## What You Get

- A directory named after the podcast
- MP3 files with dates in filenames
- A README.md tracking all episodes

## Example

```bash
# Download TED Talks
python3 podcast_downloader.py http://feeds.feedburner.com/tedtalks_video -n 10

# Result:
# TED_Talks/
# ├── 2023-12-20_Talk_Title.mp3
# ├── 2023-12-15_Another_Talk.mp3
# └── README.md
```

For more details, see README.md
