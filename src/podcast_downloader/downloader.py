#!/usr/bin/env python3
"""
Podcast Downloader - Downloads the latest N podcast episodes from an RSS feed.

Features:
- Downloads latest N episodes (default: 30)
- Creates a directory named after the podcast
- Stores downloaded episodes with proper filenames
- Maintains a README.md with metadata
- Tracks already downloaded items
"""

import os
import sys
import feedparser
import requests
import argparse
from urllib.parse import urlparse
from datetime import datetime
from pathlib import Path
import re


class PodcastDownloader:
    def __init__(self, feed_url, max_episodes=30, output_dir="."):
        """
        Initialize the downloader.

        Args:
            feed_url: URL of the podcast RSS feed
            max_episodes: Maximum number of episodes to download (default: 30)
            output_dir: Base directory for downloads (default: current directory)
        """
        self.feed_url = feed_url
        self.max_episodes = max_episodes
        self.output_dir = Path(output_dir).resolve()
        self.feed_data = None
        self.podcast_dir = None

    def fetch_feed(self):
        """Fetch and parse the RSS feed."""
        print(f"Fetching feed from {self.feed_url}...")
        try:
            self.feed_data = feedparser.parse(self.feed_url)
            if self.feed_data.bozo:
                print(f"Warning: Feed parsing issues detected: {self.feed_data.bozo_exception}")
            return True
        except Exception as e:
            print(f"Error fetching feed: {e}")
            return False

    def get_podcast_name(self):
        """Extract a safe podcast name from the feed."""
        if not self.feed_data:
            return "podcast"

        # Try to get the title from various sources
        title = self.feed_data.feed.get('title', 'podcast')

        # Clean the title to make it filesystem-safe
        # Remove invalid characters
        safe_name = re.sub(r'[\\/:*?"<>|]', '', title)
        # Replace whitespace with underscores
        safe_name = re.sub(r'\s+', '_', safe_name).strip()
        # Limit length
        safe_name = safe_name[:100]

        return safe_name

    def create_podcast_directory(self):
        """Create the directory for this podcast."""
        podcast_name = self.get_podcast_name()
        self.podcast_dir = self.output_dir / podcast_name

        # Create directory if it doesn't exist
        self.podcast_dir.mkdir(parents=True, exist_ok=True)
        print(f"Podcast directory: {self.podcast_dir}")

    def get_readme_path(self):
        """Get the path to the README.md file."""
        return self.podcast_dir / "README.md"

    def load_downloaded_items(self):
        """Load the list of already downloaded episodes from README.md."""
        readme_path = self.get_readme_path()

        if not readme_path.exists():
            return []

        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract downloaded items from the README
            # Look for lines like "- [x] Episode Title (date)"
            downloaded = []
            for line in content.split('\n'):
                if line.strip().startswith('- [x] '):
                    # Extract the episode title
                    title = line.strip()[6:]  # Remove "- [x] "
                    downloaded.append(title)

            return downloaded
        except Exception as e:
            print(f"Warning: Could not read README.md: {e}")
            return []

    def save_readme(self, downloaded_items):
        """Create or update the README.md file."""
        readme_path = self.get_readme_path()

        # Get podcast information
        feed = self.feed_data.feed
        title = feed.get('title', 'Unknown Podcast')
        description = feed.get('description', '')
        link = feed.get('link', self.feed_url)

        # Format description for markdown
        description_md = f"\n{description}\n" if description else ""

        # Create README content
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        content = f"# {title}\n\n"
        content += f"**Feed URL:** {self.feed_url}\n\n"
        content += f"**Last updated:** {now}\n\n"
        content += f"**Description:**{description_md}\n\n"
        content += "---\n\n"
        content += "## Downloaded Episodes\n\n"

        # List all episodes from the feed (up to max_episodes)
        # Use the same reversed order as download_episodes for consistency
        episodes = list(reversed(self.feed_data.entries[:self.max_episodes]))

        for episode in episodes:
            episode_title = episode.get('title', 'Untitled')
            published = episode.get('published', '')

            # Check if this episode was downloaded
            if episode_title in downloaded_items:
                status = 'x'
            else:
                status = ' '

            content += f"- [{status}] {episode_title}"
            if published:
                content += f" ({published})"
            content += "\n"

        # Write to file
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"README.md updated at {readme_path}")

    def download_episode(self, episode, index):
        """Download a single episode."""
        # Find the MP3 enclosure
        enclosure = None
        for link in episode.get('links', []):
            if link.get('type', '').startswith('audio/'):
                enclosure = link
                break

        if not enclosure:
            print(f"  Skipping: No audio enclosure found")
            return False

        audio_url = enclosure.get('href')
        audio_type = enclosure.get('type', 'mp3')

        # Get episode information
        title = episode.get('title', f"Episode_{index}")
        published = episode.get('published', '')

        # Clean the title for filename
        safe_title = re.sub(r'[\\/:*?"<>|]', '', title)
        safe_title = re.sub(r'\s+', '_', safe_title).strip()

        # Create filename with incremental index for chronological ordering
        # Format: 001_Title.mp3, 002_Title.mp3, etc.
        # This ensures alphabetical sorting = chronological order
        index_str = f"{index:03d}"  # Zero-padded to 3 digits (supports up to 999)
        filename = f"{index_str}_{safe_title}.mp3"

        filepath = self.podcast_dir / filename

        # Check if already downloaded
        if filepath.exists():
            print(f"  Skipping: {title} (already downloaded)")
            return True

        print(f"  Downloading: {title}")

        try:
            # Stream download to save memory
            response = requests.get(audio_url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # Print progress
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            sys.stdout.write(f"\r    Progress: {percent:.1f}%")
                            sys.stdout.flush()

            sys.stdout.write("\n")
            print(f"  Saved: {filepath.name}")
            return True

        except Exception as e:
            print(f"  Error downloading {title}: {e}")
            if filepath.exists():
                filepath.unlink()  # Remove partial file
            return False

    def download_episodes(self):
        """Download the latest episodes."""
        if not self.feed_data or not self.feed_data.entries:
            print("No episodes found in feed.")
            return False

        # Load already downloaded items
        downloaded_items = self.load_downloaded_items()

        # Get episodes to download (up to max_episodes)
        # RSS feeds typically return episodes in reverse chronological order (newest first)
        # We reverse them so index 1 is the oldest episode (for proper chronological ordering)
        episodes = list(reversed(self.feed_data.entries[:self.max_episodes]))

        print(f"\nFound {len(episodes)} episodes in feed.")
        print(f"Already downloaded: {len(downloaded_items)} episodes")
        print(f"Will attempt to download {len(episodes)} episodes\n")

        success_count = 0
        for i, episode in enumerate(episodes, 1):
            title = episode.get('title', f"Episode_{i}")
            print(f"{i}. {title}")

            if self.download_episode(episode, i):
                success_count += 1
                # Add to downloaded items list
                downloaded_items.append(title)

        # Update README
        self.save_readme(downloaded_items)

        print(f"\nDownload complete!")
        print(f"Successfully downloaded {success_count}/{len(episodes)} episodes")
        return True

    def run(self):
        """Run the complete download process."""
        print("=" * 60)
        print("Podcast Downloader")
        print("=" * 60)

        if not self.fetch_feed():
            return False

        self.create_podcast_directory()
        return self.download_episodes()


def main():
    parser = argparse.ArgumentParser(
        description="Download podcast episodes from an RSS feed."
    )
    parser.add_argument(
        "feed_url",
        help="URL of the podcast RSS feed"
    )
    parser.add_argument(
        "-n", "--num",
        type=int,
        default=30,
        help="Number of episodes to download (default: 30)"
    )
    parser.add_argument(
        "-o", "--output",
        default=".",
        help="Output directory (default: current directory)"
    )

    args = parser.parse_args()

    downloader = PodcastDownloader(
        feed_url=args.feed_url,
        max_episodes=args.num,
        output_dir=args.output
    )

    success = downloader.run()

    if not success:
        print("\nDownload failed.")
        sys.exit(1)

    print("\nDone!")


if __name__ == "__main__":
    main()
