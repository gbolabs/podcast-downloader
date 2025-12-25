# Podcast Downloader

A Python CLI tool to download podcast episodes from RSS feeds.

## Features

- Downloads the latest N episodes (default: 30)
- Creates organized directories named after the podcast
- Numbers files (001-999) for chronological ordering
- Tracks downloaded episodes to avoid duplicates
- Shows download progress
- Generates a README with episode metadata

## Installation

### From source

```bash
git clone https://github.com/gbo/podcast-download.git
cd podcast-download
pip install -e .
```

### Dependencies only

```bash
pip install feedparser requests
```

## Usage

### Command Line

```bash
# Download latest 30 episodes
podcast-downloader https://example.com/podcast.rss

# Download 10 episodes
podcast-downloader https://example.com/podcast.rss -n 10

# Save to specific directory
podcast-downloader https://example.com/podcast.rss -o ~/podcasts

# Combine options
podcast-downloader https://example.com/podcast.rss -n 20 -o ~/podcasts
```

### As a library

```python
from podcast_downloader import PodcastDownloader

downloader = PodcastDownloader(
    feed_url="https://example.com/podcast.rss",
    max_episodes=10,
    output_dir="./podcasts"
)
downloader.run()
```

## Output Structure

```
Podcast_Name/
├── 001_First_Episode.mp3
├── 002_Second_Episode.mp3
├── 003_Third_Episode.mp3
└── README.md
```

Files are numbered with zero-padded indices (001-999) to ensure alphabetical sorting matches chronological order.

## Project Structure

```
podcast-download/
├── src/
│   └── podcast_downloader/
│       ├── __init__.py
│       └── downloader.py
├── tests/
│   └── test_downloader.py
├── examples/
│   └── demo.py
├── pyproject.toml
├── .gitignore
└── README.md
```

## Development

### Setup

```bash
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
```

## Requirements

- Python 3.8+
- feedparser
- requests

## License

MIT
