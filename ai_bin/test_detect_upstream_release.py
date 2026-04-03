#!/usr/bin/env python3
"""
Unit tests for detect_upstream_release.py.

Tests core functionality without requiring GitHub API access.

Co-authored with AI: OpenCode (ollama-cloud/glm-5)
"""

import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from detect_upstream_release import (
    VersionParseError,
    parse_version,
    compare_versions,
    read_current_version,
    load_template,
    substitute_template,
    TemplateError,
)


class TestVersionParsing(unittest.TestCase):
    """Test version parsing and comparison."""

    def test_parse_version_standard(self):
        """Test parsing standard semantic versions."""
        self.assertEqual(parse_version("4.45.0"), (4, 45, 0))
        self.assertEqual(parse_version("1.2.3"), (1, 2, 3))
        self.assertEqual(parse_version("0.0.0"), (0, 0, 0))

    def test_parse_version_with_v_prefix(self):
        """Test parsing versions with 'v' prefix."""
        self.assertEqual(parse_version("v4.45.0"), (4, 45, 0))
        self.assertEqual(parse_version("v1.2.3"), (1, 2, 3))

    def test_parse_version_patches_to_three_parts(self):
        """Test that versions are padded to three parts."""
        self.assertEqual(parse_version("4.45"), (4, 45, 0))
        self.assertEqual(parse_version("4"), (4, 0, 0))

    def test_parse_version_invalid(self):
        """Test handling of invalid version strings."""
        with self.assertRaises(VersionParseError):
            parse_version("foo")

        with self.assertRaises(VersionParseError):
            parse_version("")

    def test_compare_versions_equal(self):
        """Test comparing equal versions."""
        self.assertEqual(compare_versions("4.45.0", "4.45.0"), 0)
        self.assertEqual(compare_versions("v4.45.0", "4.45.0"), 0)

    def test_compare_versions_less_than(self):
        """Test comparing older versions."""
        self.assertEqual(compare_versions("4.44.0", "4.45.0"), -1)
        self.assertEqual(compare_versions("4.45.0", "4.46.0"), -1)
        self.assertEqual(compare_versions("4.44.9", "4.45.0"), -1)

    def test_compare_versions_greater_than(self):
        """Test comparing newer versions."""
        self.assertEqual(compare_versions("4.46.0", "4.45.0"), 1)
        self.assertEqual(compare_versions("4.45.1", "4.45.0"), 1)
        self.assertEqual(compare_versions("5.0.0", "4.45.0"), 1)


class TestStateFile(unittest.TestCase):
    """Test state file operations."""

    def test_read_current_version_exists(self):
        """Test reading version from existing state file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("4.45.0\n")
            temp_path = Path(f.name)

        try:
            version = read_current_version(temp_path)
            self.assertEqual(version, "4.45.0")
        finally:
            temp_path.unlink()

    def test_read_current_version_not_exists(self):
        """Test reading from non-existent state file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir) / "nonexistent.txt"
            version = read_current_version(temp_path)
            self.assertIsNone(version)

    def test_read_current_version_empty(self):
        """Test reading from empty state file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("")
            temp_path = Path(f.name)

        try:
            version = read_current_version(temp_path)
            self.assertIsNone(version)
        finally:
            temp_path.unlink()

    def test_read_current_version_whitespace(self):
        """Test reading version with whitespace."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("  4.45.0  \n")
            temp_path = Path(f.name)

        try:
            version = read_current_version(temp_path)
            self.assertEqual(version, "4.45.0")
        finally:
            temp_path.unlink()


class TestTemplate(unittest.TestCase):
    """Test template loading and substitution."""

    def test_load_template_exists(self):
        """Test loading existing template."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test Template\nVersion: {VERSION}\n")
            temp_path = Path(f.name)

        try:
            content = load_template(temp_path)
            self.assertIn("{VERSION}", content)
        finally:
            temp_path.unlink()

    def test_load_template_not_exists(self):
        """Test loading non-existent template."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir) / "nonexistent.md"
            with self.assertRaises(TemplateError):
                load_template(temp_path)

    def test_substitute_template(self):
        """Test template variable substitution."""
        template = """
Title: Release {VERSION}
Date: {DATE}
Owner: {REPO_OWNER}
Compare: {COMPARE_URL}
"""
        result = substitute_template(
            template=template,
            version="4.46.0",
            commit_sha="abc123",
            published_date="2024-04-01T00:00:00Z",
            release_notes_url="https://example.com/release",
            prev_version="4.45.0",
        )

        self.assertIn("Release 4.46.0", result)
        self.assertIn("Date: 2024-04-01", result)
        self.assertIn(
            "https://github.com/gitbucket/gitbucket/compare/4.45.0...4.46.0", result
        )

    def test_substitute_template_multiple_occurrences(self):
        """Test substitution with multiple occurrences of same variable."""
        template = "{VERSION}\n{VERSION}\n{VERSION}"
        result = substitute_template(
            template=template,
            version="4.46.0",
            commit_sha="abc",
            published_date="2024-04-01",
            release_notes_url="https://example.com",
        )
        self.assertEqual(result.count("4.46.0"), 3)

    def test_substitute_template_current_placeholder(self):
        """Test that CURRENT placeholder works in compare URL."""
        template = "[Compare]({COMPARE_URL})"
        result = substitute_template(
            template=template,
            version="4.46.0",
            commit_sha="abc",
            published_date="2024-04-01",
            release_notes_url="https://example.com",
            prev_version="CURRENT",
        )
        self.assertIn("CURRENT...4.46.0", result)


class TestReleaseLogic(unittest.TestCase):
    """Test release filtering logic."""

    def test_filter_new_releases(self):
        """Test filtering releases newer than current version."""
        # Mock releases sorted by version (oldest first)
        releases = [
            {"tag_name": "4.43.0", "prerelease": False},
            {"tag_name": "4.44.0", "prerelease": False},
            {"tag_name": "4.45.0", "prerelease": False},
            {"tag_name": "4.46.0", "prerelease": False},
        ]

        current_version = "4.45.0"

        # Filter to new releases
        new_releases = [
            r for r in releases if compare_versions(r["tag_name"], current_version) > 0
        ]

        self.assertEqual(len(new_releases), 1)
        self.assertEqual(new_releases[0]["tag_name"], "4.46.0")

    def test_filter_first_run(self):
        """Test that first run processes all releases."""
        releases = [
            {"tag_name": "4.43.0", "prerelease": False},
            {"tag_name": "4.44.0", "prerelease": False},
        ]

        current_version = None

        # First run - no filtering
        if current_version is None:
            new_releases = releases
        else:
            new_releases = [
                r
                for r in releases
                if compare_versions(r["tag_name"], current_version) > 0
            ]

        self.assertEqual(len(new_releases), 2)

    def test_filter_prereleases(self):
        """Test that prereleases are filtered out."""
        releases = [
            {"tag_name": "4.44.0", "prerelease": False},
            {"tag_name": "4.45.0-beta", "prerelease": True},
            {"tag_name": "4.45.0-rc1", "prerelease": True},
            {"tag_name": "4.45.0", "prerelease": False},
        ]

        # Filter to stable releases
        stable = [r for r in releases if not r.get("prerelease", False)]

        self.assertEqual(len(stable), 2)
        self.assertEqual(stable[0]["tag_name"], "4.44.0")
        self.assertEqual(stable[1]["tag_name"], "4.45.0")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def test_version_comparison_different_lengths(self):
        """Test comparing versions with different number of parts."""
        self.assertEqual(compare_versions("4", "4.0"), 0)
        self.assertEqual(compare_versions("4.45", "4.45.0"), 0)

    def test_version_with_extra_text(self):
        """Test parsing version with extra text."""
        # Should extract numeric parts
        result = parse_version("v4.45.0")
        self.assertEqual(result, (4, 45, 0))

    def test_empty_release_list(self):
        """Test handling empty release list."""
        releases = []
        current_version = "4.45.0"

        new_releases = [
            r for r in releases if compare_versions(r["tag_name"], current_version) > 0
        ]

        self.assertEqual(len(new_releases), 0)

    def test_template_missing_variable(self):
        """Test substitution when variable not in template."""
        template = "No variables here"
        result = substitute_template(
            template=template,
            version="4.46.0",
            commit_sha="abc",
            published_date="2024-04-01",
            release_notes_url="https://example.com",
        )
        self.assertEqual(result, "No variables here")


if __name__ == "__main__":
    unittest.main()
