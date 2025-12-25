#!/usr/bin/env python3
"""
Podcast Downloader - Downloads the latest N podcast episodes from an RSS feed.

Features:
- Downloads latest N episodes (default: 30)
- Creates a directory named after the podcast
- Stores downloaded episodes with proper filenames
- Maintains a README.md with metadata
- Tracks already downloaded items
- Smart filename truncation for devices with length limits
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
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

try:
    from unidecode import unidecode
except ImportError:
    unidecode = None


# Stop words to remove when shortening titles (multilingual)
STOP_WORDS = {
    # French
    'le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'et', 'en', 'au', 'aux',
    'ce', 'cette', 'ces', 'son', 'sa', 'ses', 'mon', 'ma', 'mes', 'ton', 'ta',
    'tes', 'notre', 'nos', 'votre', 'vos', 'leur', 'leurs', 'qui', 'que', 'quoi',
    'dont', 'où', 'pour', 'par', 'sur', 'sous', 'avec', 'sans', 'dans', 'est',
    # English
    'the', 'a', 'an', 'of', 'to', 'and', 'in', 'on', 'at', 'for', 'with',
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
    'this', 'that', 'these', 'those', 'it', 'its',
}


class TitleShortener:
    """Intelligently shortens titles while preserving meaning."""

    def __init__(self, max_length, preserve_numbers=True):
        self.max_length = max_length
        self.preserve_numbers = preserve_numbers

    def shorten(self, title, prefix_length=0):
        """
        Shorten a title to fit within max_length (including prefix).

        Args:
            title: The original title
            prefix_length: Length of prefix (e.g., "01_") to account for

        Returns:
            Shortened title that fits within max_length - prefix_length - 4 (.mp3)
        """
        available = self.max_length - prefix_length - 4  # -4 for ".mp3"
        if available <= 0:
            return ""

        # Clean the title first
        cleaned = self._clean_title(title)

        if len(cleaned) <= available:
            return cleaned

        # Strategy 1: Remove stop words
        shortened = self._remove_stop_words(cleaned)
        if len(shortened) <= available:
            return shortened

        # Strategy 2: Abbreviate long words (keep first 4 chars)
        shortened = self._abbreviate_words(shortened, min_word_length=6)
        if len(shortened) <= available:
            return shortened

        # Strategy 3: More aggressive abbreviation (keep first 3 chars)
        shortened = self._abbreviate_words(shortened, min_word_length=5, keep_chars=3)
        if len(shortened) <= available:
            return shortened

        # Strategy 4: Truncate at word boundary
        shortened = self._truncate_at_word_boundary(shortened, available)
        return shortened

    def _clean_title(self, title):
        """Clean title: remove special chars, normalize spaces."""
        # Convert accented chars to ASCII if unidecode is available
        if unidecode:
            title = unidecode(title)

        # Remove special characters but keep alphanumeric and spaces
        cleaned = re.sub(r'[^\w\s-]', '', title)
        # Replace whitespace with underscores
        cleaned = re.sub(r'\s+', '_', cleaned).strip('_')
        # Remove multiple underscores
        cleaned = re.sub(r'_+', '_', cleaned)
        return cleaned

    def _remove_stop_words(self, title):
        """Remove stop words from title."""
        words = title.split('_')
        filtered = []
        for word in words:
            word_lower = word.lower()
            # Keep numbers and non-stop words
            if word_lower not in STOP_WORDS or word.isdigit():
                filtered.append(word)
        return '_'.join(filtered) if filtered else title

    def _abbreviate_words(self, title, min_word_length=6, keep_chars=4):
        """Abbreviate words longer than min_word_length."""
        words = title.split('_')
        abbreviated = []
        for word in words:
            if len(word) > min_word_length and not word.isdigit():
                abbreviated.append(word[:keep_chars])
            else:
                abbreviated.append(word)
        return '_'.join(abbreviated)

    def _truncate_at_word_boundary(self, title, max_length):
        """Truncate at word boundary."""
        if len(title) <= max_length:
            return title

        words = title.split('_')
        result = []
        current_length = 0

        for word in words:
            # +1 for underscore separator
            new_length = current_length + len(word) + (1 if result else 0)
            if new_length <= max_length:
                result.append(word)
                current_length = new_length
            else:
                break

        return '_'.join(result) if result else title[:max_length]


class PodcastDownloader:
    def __init__(self, feed_url, max_episodes=30, output_dir=".", max_filename_length=None, parallel=2):
        """
        Initialize the downloader.

        Args:
            feed_url: URL of the podcast RSS feed
            max_episodes: Maximum number of episodes to download (default: 30)
            output_dir: Base directory for downloads (default: current directory)
            max_filename_length: Maximum filename length for devices with limits (default: None = no limit)
            parallel: Number of parallel downloads (default: 2, use 1 for sequential)
        """
        self.feed_url = feed_url
        self.max_episodes = max_episodes
        self.output_dir = Path(output_dir).resolve()
        self.max_filename_length = max_filename_length
        self.parallel = max(1, parallel)
        self.feed_data = None
        self.podcast_dir = None
        self.shortener = TitleShortener(max_filename_length) if max_filename_length else None

        # Create a session for connection pooling (faster repeated requests)
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=self.parallel,
            pool_maxsize=self.parallel * 2,
            max_retries=3
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        # Thread-safe print lock
        self._print_lock = threading.Lock()

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
        """Extract a safe podcast name from the feed, respecting max_filename_length."""
        if not self.feed_data:
            return "podcast"

        # Try to get the title from various sources
        title = self.feed_data.feed.get('title', 'podcast')

        # Use smart shortening if max_filename_length is set
        if self.shortener:
            # For folder name, use the full max_length (no prefix, no extension)
            folder_shortener = TitleShortener(self.max_filename_length)
            safe_name = folder_shortener._clean_title(title)

            if len(safe_name) > self.max_filename_length:
                safe_name = folder_shortener._remove_stop_words(safe_name)
            if len(safe_name) > self.max_filename_length:
                safe_name = folder_shortener._abbreviate_words(safe_name, min_word_length=6)
            if len(safe_name) > self.max_filename_length:
                safe_name = folder_shortener._truncate_at_word_boundary(safe_name, self.max_filename_length)

            return safe_name
        else:
            # Default: clean but don't limit length
            safe_name = re.sub(r'[\\/:*?"<>|]', '', title)
            safe_name = re.sub(r'\s+', '_', safe_name).strip()
            safe_name = safe_name[:100]
            return safe_name

    def create_podcast_directory(self):
        """Create the directory for this podcast (called after knowing episode count)."""
        # podcast_dir is set dynamically per batch in download_episode
        # This just stores the base podcast name
        self.podcast_name = self.get_podcast_name()
        print(f"Podcast: {self.podcast_name}")

    def _get_batch_folder(self, index, total_count):
        """
        Get the folder path for an episode based on batching.

        For ≤100 episodes: just podcast_name/
        For >100 episodes: N_podcast_name/ where N is batch number (0, 1, 2...)
        Each batch contains up to 100 files (00-99).
        """
        if total_count <= 100:
            return self.output_dir / self.podcast_name

        # Calculate batch number (0-indexed, 100 files per batch)
        batch_num = (index - 1) // 100
        folder_name = f"{batch_num}_{self.podcast_name}"

        return self.output_dir / folder_name

    def get_readme_path(self, total_count=1):
        """Get the path to the README.md file (in the first/main folder)."""
        folder = self._get_batch_folder(1, total_count)
        return folder / "README.md"

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

    def save_readme(self, downloaded_items, total_count):
        """Create or update the README.md file."""
        readme_path = self.get_readme_path(total_count)

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

    def _get_index_width(self, count):
        """Calculate the minimum width needed for zero-padded indices."""
        if count <= 9:
            return 1
        elif count <= 99:
            return 2
        else:
            return 3

    def download_episode(self, episode, index, total_count):
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

        # Get target folder (may be batched for >100 episodes)
        target_dir = self._get_batch_folder(index, total_count)
        target_dir.mkdir(parents=True, exist_ok=True)

        # Calculate display index within batch
        if total_count <= 100:
            # Single folder: use dynamic width based on count
            index_width = self._get_index_width(total_count)
            display_index = index
        else:
            # Batched folders: always 00-99 within each batch
            index_width = 2
            display_index = (index - 1) % 100  # 0-99 within batch

        # Create filename with appropriate index
        index_str = f"{display_index:0{index_width}d}"
        prefix = f"{index_str}_"

        # Use smart shortening if max_filename_length is set
        if self.shortener:
            safe_title = self.shortener.shorten(title, prefix_length=len(prefix))
        else:
            # Default cleaning without length limit
            safe_title = re.sub(r'[\\/:*?"<>|]', '', title)
            safe_title = re.sub(r'\s+', '_', safe_title).strip()

        filename = f"{prefix}{safe_title}.mp3"

        filepath = target_dir / filename

        # Check if already downloaded
        if filepath.exists():
            with self._print_lock:
                print(f"  [{index:02d}] Skipping: {title[:40]}... (exists)")
            return (index, title, True, "skipped")

        with self._print_lock:
            print(f"  [{index:02d}] Downloading: {title[:40]}...")

        try:
            # Stream download using session (connection pooling)
            response = self.session.get(audio_url, stream=True, timeout=(10, 60))
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=65536):  # Larger chunks
                    if chunk:
                        f.write(chunk)

            with self._print_lock:
                size_mb = total_size / (1024 * 1024) if total_size else 0
                print(f"  [{index:02d}] Done: {filepath.name} ({size_mb:.1f} MB)")
            return (index, title, True, "downloaded")

        except Exception as e:
            with self._print_lock:
                print(f"  [{index:02d}] Error: {title[:30]}... - {e}")
            if filepath.exists():
                filepath.unlink()  # Remove partial file
            return (index, title, False, str(e))

    def download_episodes(self):
        """Download the latest episodes (parallel or sequential)."""
        if not self.feed_data or not self.feed_data.entries:
            print("No episodes found in feed.")
            return False

        # Load already downloaded items
        downloaded_items = self.load_downloaded_items()

        # Get episodes to download (up to max_episodes)
        # RSS feeds typically return episodes in reverse chronological order (newest first)
        # We reverse them so index 1 is the oldest episode (for proper chronological ordering)
        episodes = list(reversed(self.feed_data.entries[:self.max_episodes]))
        total_count = len(episodes)

        print(f"\nFound {total_count} episodes in feed.")
        print(f"Already downloaded: {len(downloaded_items)} episodes")
        print(f"Downloading with {self.parallel} parallel connections...\n")

        import time
        start_time = time.time()

        success_count = 0
        download_count = 0

        # Prepare download tasks: (episode, index, total_count)
        tasks = [(ep, i, total_count) for i, ep in enumerate(episodes, 1)]

        # Use ThreadPoolExecutor for parallel downloads
        with ThreadPoolExecutor(max_workers=self.parallel) as executor:
            # Submit all download tasks
            futures = {
                executor.submit(self.download_episode, ep, idx, total): (idx, ep)
                for ep, idx, total in tasks
            }

            # Process completed downloads
            for future in as_completed(futures):
                idx, ep = futures[future]
                try:
                    result = future.result()
                    index, title, success, status = result
                    if success:
                        success_count += 1
                        downloaded_items.append(title)
                        if status == "downloaded":
                            download_count += 1
                except Exception as e:
                    print(f"  Task error: {e}")

        elapsed = time.time() - start_time

        # Update README
        self.save_readme(downloaded_items, total_count)

        print(f"\nDownload complete in {elapsed:.1f}s")
        print(f"Downloaded: {download_count}, Skipped: {success_count - download_count}, Failed: {total_count - success_count}")
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
    parser.add_argument(
        "-m", "--max-length",
        type=int,
        default=None,
        help="Maximum filename length for devices with limits (e.g., 27 for Remi babyphone)"
    )
    parser.add_argument(
        "-p", "--parallel",
        type=int,
        default=2,
        help="Number of parallel downloads (default: 2)"
    )

    args = parser.parse_args()

    downloader = PodcastDownloader(
        feed_url=args.feed_url,
        max_episodes=args.num,
        output_dir=args.output,
        max_filename_length=args.max_length,
        parallel=args.parallel
    )

    success = downloader.run()

    if not success:
        print("\nDownload failed.")
        sys.exit(1)

    print("\nDone!")


if __name__ == "__main__":
    main()
