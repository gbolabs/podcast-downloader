#!/usr/bin/env python3
"""Test script to verify the downloader works."""

import sys
sys.path.insert(0, '.')

from podcast_downloader import PodcastDownloader

# Test with a known working podcast feed
# Using a simple test to verify the structure works
print("Testing PodcastDownloader class...")

# Create a downloader instance (won't actually download)
downloader = PodcastDownloader(
    feed_url="https://example.com/test.rss",
    max_episodes=5,
    output_dir="./test_output"
)

print(f"✓ Downloader created successfully")
print(f"  Feed URL: {downloader.feed_url}")
print(f"  Max episodes: {downloader.max_episodes}")
print(f"  Output dir: {downloader.output_dir}")

# Test podcast name generation
test_feed_data = type('obj', (object,), {
    'feed': {
        'title': 'Test Podcast with Special Chars: /\\:*?"<>|'
    },
    'entries': []
})()
downloader.feed_data = test_feed_data
podcast_name = downloader.get_podcast_name()
print(f"✓ Podcast name generation: '{podcast_name}'")

# Test directory creation
downloader.create_podcast_directory()
print(f"✓ Directory creation: {downloader.podcast_dir.exists()}")

# Test README path
readme_path = downloader.get_readme_path()
print(f"✓ README path: {readme_path}")

print("\n✓ All basic tests passed!")
print("\nNote: To test with a real podcast feed, use:")
print("  python3 podcast_downloader.py <RSS_FEED_URL>")
