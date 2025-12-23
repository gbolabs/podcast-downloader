#!/usr/bin/env python3
"""
Demonstration of the Podcast Downloader functionality.
This script shows what happens when you run the downloader.
"""

import os
import shutil
from pathlib import Path

print("=" * 70)
print("PODCAST DOWNLOADER - DEMONSTRATION")
print("=" * 70)

print("\n1. Application Structure")
print("-" * 70)
print("The application consists of:")
print("  - podcast_downloader.py (main script)")
print("  - README.md (this documentation)")
print("  - EXAMPLE_OUTPUT.md (example output format)")

print("\n2. How to Use")
print("-" * 70)
print("Basic command:")
print("  $ python3 podcast_downloader.py <RSS_FEED_URL>")
print("\nWith options:")
print("  $ python3 podcast_downloader.py <RSS_FEED_URL> -n 20 -o ~/podcasts")
print("    -n 20: Download 20 episodes (default: 30)")
print("    -o ~/podcasts: Save to ~/podcasts directory")

print("\n3. What Happens When You Run It")
print("-" * 70)
print("Step 1: Fetch the RSS feed")
print("  → Parses the feed to get podcast information and episode list")
print("")
print("Step 2: Create podcast directory")
print("  → Creates a directory named after the podcast")
print("  Example: 'The_Daily_Tech_News/'")
print("")
print("Step 3: Download episodes")
print("  → Downloads MP3 files with names like:")
print("    - 2023-01-15_Episode_Title.mp3")
print("    - 2023-01-10_Another_Episode.mp3")
print("")
print("Step 4: Create/Update README.md")
print("  → Generates a README with:")
print("    - Podcast title and description")
print("    - Feed URL")
print("    - List of episodes with checkboxes")
print("    - Last update timestamp")

print("\n4. Example Output Structure")
print("-" * 70)
print("The_Daily_Tech_News/")
print("├── 2023-01-15_Episode_123.mp3")
print("├── 2023-01-10_Episode_122.mp3")
print("├── 2023-01-05_Episode_121.mp3")
print("└── README.md")

print("\n5. Running the Test")
print("-" * 70)

# Run the test script
import subprocess
result = subprocess.run(['python3', 'test_downloader.py'], capture_output=False)

print("\n6. Key Features")
print("-" * 70)
print("✓ Downloads latest N episodes (configurable, default: 30)")
print("✓ Creates organized directory structure")
print("✓ Generates descriptive filenames with dates")
print("✓ Tracks downloaded episodes in README.md")
print("✓ Avoids re-downloading existing files")
print("✓ Handles special characters in titles safely")
print("✓ Shows download progress")

print("\n7. Try It Yourself")
print("-" * 70)
print("You can test with real podcast feeds like:")
print("  - TED Talks: http://feeds.feedburner.com/tedtalks_video")
print("  - Stuff You Should Know: http://feeds.stuffyoushouldknow.com/stuffyoushouldknow")
print("  - Any podcast RSS feed URL")

print("\n" + "=" * 70)
print("Demo complete!")
print("=" * 70)
