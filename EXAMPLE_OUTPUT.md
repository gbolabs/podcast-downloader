# Example Output Structure

When you run the podcast downloader, it creates a directory structure like this:

```
Podcast_Name/
├── 2023-01-15_Episode_Title.mp3
├── 2023-01-10_Another_Episode.mp3
├── ...
└── README.md
```

## Example README.md Content

Here's what the generated README.md would look like:

```markdown
# The Daily Tech News

**Feed URL:** https://example.com/podcast.rss

**Last updated:** 2023-12-23 15:30:45

**Description:**
The latest in technology news, delivered daily.

---

## Downloaded Episodes

- [x] Episode 123: AI Breakthroughs in 2023 (Mon, 15 Jan 2023 08:00:00 GMT)
- [x] Episode 122: Quantum Computing Update (Wed, 11 Jan 2023 08:00:00 GMT)
- [x] Episode 121: New Smartphone Releases (Mon, 09 Jan 2023 08:00:00 GMT)
- [ ] Episode 120: Cybersecurity Trends (Fri, 05 Jan 2023 08:00:00 GMT)
- [ ] Episode 119: Year in Review (Wed, 03 Jan 2023 08:00:00 GMT)
```

## How to Use This Application

### 1. Install Dependencies

```bash
pip install feedparser requests
```

### 2. Run the Downloader

```bash
python3 podcast_downloader.py https://example.com/podcast.rss
```

### 3. Customize Downloads

Download 20 episodes to a specific directory:

```bash
python3 podcast_downloader.py https://example.com/podcast.rss -n 20 -o ~/my_podcasts
```

### 4. Re-run to Update

When you run the downloader again, it will:
- Skip episodes that already exist
- Update the README.md with new episodes
- Mark downloaded episodes with [x] checkboxes
- Add new episodes to the list

## Features

- **Smart Filename Generation**: Uses publication date when available
- **Duplicate Prevention**: Checks for existing files before downloading
- **Metadata Tracking**: README.md keeps track of all episodes
- **Progress Indicators**: Shows download progress for each episode
- **Filesystem Safety**: Cleans special characters from filenames

## Troubleshooting

If you encounter issues:

1. **Check the feed URL**: Make sure it's a valid RSS feed
2. **Verify network access**: Ensure you can reach the feed URL
3. **Check permissions**: Make sure you have write access to the output directory
4. **Review logs**: The application prints detailed progress information

## Example with Real Podcasts

Here are some real podcast feeds you can try:

- **BBC Radio 4 Today**: `https://feeds.bbci.co.uk/podcasts/series/radio4today/rss.xml`
- **TED Talks Daily**: `http://feeds.feedburner.com/tedtalks_video`
- **Stuff You Should Know**: `http://feeds.stuffyoushouldknow.com/stuffyoushouldknow`
