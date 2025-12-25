# Podcast Downloader

A Python CLI tool to download podcast episodes from RSS feeds.

## Features

- Downloads the latest N episodes (default: 30)
- Creates organized directories named after the podcast
- Dynamic numbering (1-9, 01-99, 001-999) based on episode count
- **Remi babyphone compatibility** (`-m 27` option):
  - Smart filename shortening to fit device display limits
  - Converts accents to ASCII (é→e, ô→o)
  - Removes stop words (le, la, the, of...)
  - Abbreviates long words intelligently
  - Sibling folder batching for 100+ episodes (no subfolders needed)
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

# For Remi babyphone (27-char filename limit)
podcast-downloader https://example.com/podcast.rss -m 27

# Combine options
podcast-downloader https://example.com/podcast.rss -n 20 -o ~/podcasts -m 27
```

### As a library

```python
from podcast_downloader import PodcastDownloader

downloader = PodcastDownloader(
    feed_url="https://example.com/podcast.rss",
    max_episodes=10,
    output_dir="./podcasts",
    max_filename_length=27  # Optional: for devices with filename limits
)
downloader.run()
```

## Output Structure

For up to 100 episodes:
```
Podcast_Name/
├── 01_First_Episode.mp3
├── 02_Second_Episode.mp3
├── ...
└── README.md
```

For 100+ episodes (sibling folders, 100 files each):
```
0_Podcast_Name/
├── 00_Episode_1.mp3
├── 01_Episode_2.mp3
└── 99_Episode_100.mp3

1_Podcast_Name/
├── 00_Episode_101.mp3
└── 49_Episode_150.mp3
```

This sibling folder structure is designed for devices like **Remi babyphone** that:
- Have a ~27 character filename display limit
- Support folders but not nested subfolders
- Sort files alphabetically

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
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Or use requirements.txt
pip install -r requirements.txt
pip install -e .
```

### VS Code

The project includes VS Code configurations for debugging:

1. Open the project in VS Code
2. Select the Python interpreter from `.venv`
3. Use the Run and Debug panel (F5) with these configurations:
   - **Python: Download Podcast** - Debug the CLI with sample args
   - **Python: Current File** - Debug any open file
   - **Python: Debug Tests** - Debug pytest tests

### Run tests

```bash
pytest
```

## Requirements

- Python 3.8+
- feedparser
- requests
- unidecode (for smart filename shortening)

## License

MIT
