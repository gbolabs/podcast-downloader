# Podcast Downloader

A simple Python application to download podcast episodes from RSS feeds.

## Features

- Downloads the latest N podcast episodes (default: 30)
- Creates a directory named after the podcast
- Stores downloaded episodes with proper filenames
- Maintains a README.md with metadata
- Tracks already downloaded items to avoid duplicates
- Shows download progress

## Requirements

- Python 3.6+
- `feedparser` library
- `requests` library

Install dependencies:
```bash
pip install feedparser requests
```

## Usage

### Basic Usage

Download the latest 30 episodes from a podcast feed:
```bash
python podcast_downloader.py https://example.com/podcast.rss
```

### Download Specific Number of Episodes

Download only 10 episodes:
```bash
python podcast_downloader.py https://example.com/podcast.rss -n 10
```

### Specify Output Directory

Save episodes to a specific directory:
```bash
python podcast_downloader.py https://example.com/podcast.rss -o ~/podcasts
```

### Combine Options

```bash
python podcast_downloader.py https://example.com/podcast.rss -n 20 -o ~/podcasts
```

## How It Works

1. **Fetch Feed**: Downloads and parses the RSS feed
2. **Create Directory**: Creates a directory named after the podcast
3. **Download Episodes**: Downloads the latest N episodes as MP3 files
4. **Create README**: Generates a README.md file with:
   - Podcast title and description
   - Feed URL
   - List of downloaded episodes (marked with checkboxes)
   - Last update timestamp

## Example Output

```
Podcast_Name/
├── 2023-01-15_Episode_123.mp3
├── 2023-01-10_Episode_122.mp3
├── ...
└── README.md
```

**Note:** Episode files are named with dates in `YYYY-MM-DD` format, which ensures they sort chronologically when listed alphabetically. See [000_CHRONOLOGICAL_SORTING_DEMO.md](000_CHRONOLOGICAL_SORTING_DEMO.md) for more details.

The README.md will contain:
- Podcast information
- Feed URL
- List of episodes with checkboxes indicating which are downloaded

## Notes

- The application checks for existing files and skips re-downloading them
- Episode filenames include the publication date when available
- Invalid characters in titles are replaced with underscores for filesystem safety
- The README.md is updated after each run to reflect the current state

## License

This is a simple utility script. Feel free to use and modify it as needed.
