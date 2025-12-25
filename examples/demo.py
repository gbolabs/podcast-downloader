#!/usr/bin/env python3
"""
Example usage of the Podcast Downloader.

This script demonstrates how to use the PodcastDownloader programmatically.
"""

from podcast_downloader import PodcastDownloader


def main():
    print("=" * 60)
    print("Podcast Downloader - Example Usage")
    print("=" * 60)

    # Example 1: Basic usage
    print("\n1. Basic Usage")
    print("-" * 60)
    print("""
    from podcast_downloader import PodcastDownloader

    downloader = PodcastDownloader(
        feed_url="https://example.com/podcast.rss",
        max_episodes=10,
        output_dir="./podcasts"
    )
    downloader.run()
    """)

    # Example 2: Command-line usage
    print("\n2. Command-Line Usage")
    print("-" * 60)
    print("""
    # Download latest 30 episodes (default)
    $ podcast-downloader https://example.com/podcast.rss

    # Download only 10 episodes
    $ podcast-downloader https://example.com/podcast.rss -n 10

    # Save to a specific directory
    $ podcast-downloader https://example.com/podcast.rss -o ~/podcasts

    # Combine options
    $ podcast-downloader https://example.com/podcast.rss -n 20 -o ~/podcasts
    """)

    # Example 3: Output structure
    print("\n3. Output Structure")
    print("-" * 60)
    print("""
    After running, you'll get:

    Podcast_Name/
    ├── 001_First_Episode.mp3
    ├── 002_Second_Episode.mp3
    ├── 003_Third_Episode.mp3
    └── README.md

    Files are numbered (001-999) to ensure alphabetical sorting
    matches chronological order.
    """)

    # Example 4: Sample podcast feeds
    print("\n4. Sample Podcast Feeds to Try")
    print("-" * 60)
    print("""
    Try with these public podcast feeds:

    - TED Talks Daily:
      https://feeds.feedburner.com/tedtalks_audio

    - Stuff You Should Know:
      https://feeds.megaphone.fm/stuffyoushouldknow

    - The Daily (NYT):
      https://feeds.simplecast.com/54nAGcIl
    """)

    print("=" * 60)
    print("Run 'podcast-downloader --help' for more options")
    print("=" * 60)


if __name__ == "__main__":
    main()
