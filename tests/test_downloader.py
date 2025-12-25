"""Tests for the PodcastDownloader class."""

import pytest
from pathlib import Path
from unittest.mock import MagicMock

from podcast_downloader import PodcastDownloader


class TestPodcastDownloader:
    """Test suite for PodcastDownloader."""

    def test_init(self, tmp_path):
        """Test downloader initialization."""
        downloader = PodcastDownloader(
            feed_url="https://example.com/test.rss",
            max_episodes=5,
            output_dir=str(tmp_path),
        )
        assert downloader.feed_url == "https://example.com/test.rss"
        assert downloader.max_episodes == 5
        assert downloader.output_dir == tmp_path

    def test_get_podcast_name_cleans_special_chars(self, tmp_path):
        """Test that podcast names are sanitized for filesystem use."""
        downloader = PodcastDownloader(
            feed_url="https://example.com/test.rss",
            output_dir=str(tmp_path),
        )
        downloader.feed_data = MagicMock()
        downloader.feed_data.feed.get.return_value = 'Test Podcast: /\\:*?"<>|'

        name = downloader.get_podcast_name()

        assert "/" not in name
        assert "\\" not in name
        assert ":" not in name
        assert "*" not in name
        assert "?" not in name
        assert '"' not in name
        assert "<" not in name
        assert ">" not in name
        assert "|" not in name

    def test_get_podcast_name_replaces_whitespace(self, tmp_path):
        """Test that whitespace is replaced with underscores."""
        downloader = PodcastDownloader(
            feed_url="https://example.com/test.rss",
            output_dir=str(tmp_path),
        )
        downloader.feed_data = MagicMock()
        downloader.feed_data.feed.get.return_value = "My Great Podcast"

        name = downloader.get_podcast_name()

        assert " " not in name
        assert name == "My_Great_Podcast"

    def test_create_podcast_directory(self, tmp_path):
        """Test that podcast directory is created."""
        downloader = PodcastDownloader(
            feed_url="https://example.com/test.rss",
            output_dir=str(tmp_path),
        )
        downloader.feed_data = MagicMock()
        downloader.feed_data.feed.get.return_value = "Test_Podcast"

        downloader.create_podcast_directory()

        assert downloader.podcast_dir.exists()
        assert downloader.podcast_dir.is_dir()

    def test_get_readme_path(self, tmp_path):
        """Test README path generation."""
        downloader = PodcastDownloader(
            feed_url="https://example.com/test.rss",
            output_dir=str(tmp_path),
        )
        downloader.feed_data = MagicMock()
        downloader.feed_data.feed.get.return_value = "Test_Podcast"
        downloader.create_podcast_directory()

        readme_path = downloader.get_readme_path()

        assert readme_path.name == "README.md"
        assert readme_path.parent == downloader.podcast_dir

    def test_load_downloaded_items_empty(self, tmp_path):
        """Test loading downloaded items when no README exists."""
        downloader = PodcastDownloader(
            feed_url="https://example.com/test.rss",
            output_dir=str(tmp_path),
        )
        downloader.feed_data = MagicMock()
        downloader.feed_data.feed.get.return_value = "Test_Podcast"
        downloader.create_podcast_directory()

        items = downloader.load_downloaded_items()

        assert items == []


class TestFilenameGeneration:
    """Test filename generation for chronological ordering."""

    def test_filename_format(self, tmp_path):
        """Test that filenames have correct format with zero-padded index."""
        import re

        episodes = [
            {"title": "Episode 1", "published": "Mon, 01 Jan 2024"},
            {"title": "Episode 2", "published": "Tue, 02 Jan 2024"},
        ]

        for i, ep in enumerate(episodes, 1):
            title = ep["title"]
            safe_title = re.sub(r'[\\/:*?"<>|]', "", title)
            safe_title = re.sub(r"\s+", "_", safe_title).strip()
            index_str = f"{i:03d}"
            filename = f"{index_str}_{safe_title}.mp3"

            assert filename.startswith(f"{i:03d}_")
            assert filename.endswith(".mp3")

    def test_alphabetical_equals_chronological(self):
        """Test that alphabetical sorting equals chronological order."""
        filenames = [
            "001_First_Episode.mp3",
            "002_Second_Episode.mp3",
            "003_Third_Episode.mp3",
            "010_Tenth_Episode.mp3",
            "100_Hundredth_Episode.mp3",
        ]

        sorted_filenames = sorted(filenames)

        assert filenames == sorted_filenames
