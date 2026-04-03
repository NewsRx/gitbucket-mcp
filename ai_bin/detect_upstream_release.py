#!/usr/bin/env python3
"""
Detect upstream GitBucket releases and create GitHub issues.

This script replaces the shell-based workflow in .github/workflows/detect-upstream-release.yml
with Python for improved maintainability, testability, and error handling.

Workflow:
1. Fetch releases from gitbucket/gitbucket upstream
2. Compare against workflow-state/last_release.txt
3. Filter to stable releases newer than current version
4. Create GitHub issues using template for each new release

Co-authored with AI: OpenCode (ollama-cloud/glm-5)
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class VersionParseError(ValueError):
    """Raised when version string cannot be parsed."""

    pass


class ReleaseDetectionError(Exception):
    """Raised when release detection fails."""

    pass


class StateFileError(Exception):
    """Raised when state file operations fail."""

    pass


class TemplateError(Exception):
    """Raised when template substitution fails."""

    pass


class GitHubAPIError(Exception):
    """Raised when GitHub API calls fail."""

    pass


def parse_version(version_str: str) -> tuple[int, int, int]:
    """
    Parse semantic version string to tuple.

    Args:
        version_str: Version string like "4.45.0" or "v4.45.0"

    Returns:
        Tuple of (major, minor, patch) integers

    Raises:
        VersionParseError: If version cannot be parsed
    """
    # Remove 'v' prefix if present
    cleaned = version_str.lstrip("v")

    # Extract numeric parts
    parts = re.findall(r"\d+", cleaned)

    if len(parts) < 1:
        raise VersionParseError(f"Cannot parse version: {version_str}")

    # Pad to at least 3 parts (major, minor, patch)
    while len(parts) < 3:
        parts.append("0")

    try:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError as e:
        raise VersionParseError(f"Cannot parse version: {version_str}") from e


def compare_versions(v1: str, v2: str) -> int:
    """
    Compare two semantic versions.

    Args:
        v1: First version string
        v2: Second version string

    Returns:
        -1 if v1 < v2, 0 if v1 == v2, 1 if v1 > v2

    Raises:
        VersionParseError: If either version cannot be parsed
    """
    p1 = parse_version(v1)
    p2 = parse_version(v2)

    if p1 < p2:
        return -1
    elif p1 > p2:
        return 1
    else:
        return 0


def read_current_version(state_file: Path) -> Optional[str]:
    """
    Read last processed version from state file.

    Args:
        state_file: Path to state file (workflow-state/last_release.txt)

    Returns:
        Version string or None if file doesn't exist

    Raises:
        StateFileError: If file read fails
    """
    if not state_file.exists():
        logger.info(f"State file {state_file} not found, treating as first run")
        return None

    try:
        content = state_file.read_text().strip()
        if not content:
            logger.warning(f"State file {state_file} is empty")
            return None

        # Extract version from content (handle "4.45.0" format)
        version = content.strip()
        logger.info(f"Current tracked version: {version}")
        return version

    except Exception as e:
        raise StateFileError(f"Failed to read state file {state_file}: {e}") from e


def github_api_get(url: str, token: str) -> dict:
    """
    Make authenticated GitHub API GET request using urllib.

    Args:
        url: GitHub API URL
        token: GitHub token

    Returns:
        JSON response as dict

    Raises:
        GitHubAPIError: If request fails
    """
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "gitbucket-mcp-release-detector",
    }

    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
    except urllib.error.HTTPError as e:
        raise GitHubAPIError(
            f"GitHub API request failed: HTTP {e.code} {e.reason}"
        ) from e
    except urllib.error.URLError as e:
        raise GitHubAPIError(f"GitHub API request failed: {e.reason}") from e
    except json.JSONDecodeError as e:
        raise GitHubAPIError(f"Failed to parse GitHub API response: {e}") from e


def fetch_releases(token: str, current_version: Optional[str]) -> list[dict]:
    """
    Fetch new stable releases from gitbucket/gitbucket.

    Args:
        token: GitHub API token
        current_version: Last processed version (None for first run)

    Returns:
        List of release dictionaries sorted by version (oldest first)

    Raises:
        ReleaseDetectionError: If release fetch fails
    """
    try:
        url = "https://api.github.com/repos/gitbucket/gitbucket/releases?per_page=100"
        all_releases = github_api_get(url, token)

        logger.info(
            f"Fetched {len(all_releases)} total releases from gitbucket/gitbucket"
        )

        # Filter to stable releases only
        stable_releases = [r for r in all_releases if not r.get("prerelease", False)]
        logger.info(f"Found {len(stable_releases)} stable releases")

        # Sort by version (oldest first for processing)
        def get_version_tuple(r):
            try:
                return parse_version(r["tag_name"])
            except VersionParseError:
                # If version can't be parsed, put it at the end
                return (9999, 9999, 9999)

        stable_releases.sort(key=get_version_tuple)

        # Filter to new releases if current_version exists
        if current_version:
            new_releases = [
                r
                for r in stable_releases
                if compare_versions(r["tag_name"], current_version) > 0
            ]
            logger.info(
                f"Found {len(new_releases)} releases newer than {current_version}"
            )
            return new_releases
        else:
            # First run - process all releases
            logger.info(
                f"First run, processing all {len(stable_releases)} stable releases"
            )
            return stable_releases

    except GitHubAPIError as e:
        raise ReleaseDetectionError(f"Failed to fetch releases: {e}") from e


def load_template(template_path: Path) -> str:
    """
    Load issue template content.

    Args:
        template_path: Path to .github/ISSUE_TEMPLATE/upstream-release.md

    Returns:
        Template content

    Raises:
        TemplateError: If template cannot be loaded
    """
    if not template_path.exists():
        raise TemplateError(f"Template file not found: {template_path}")

    try:
        return template_path.read_text()
    except Exception as e:
        raise TemplateError(f"Failed to read template {template_path}: {e}") from e


def substitute_template(
    template: str,
    version: str,
    commit_sha: str,
    published_date: str,
    release_notes_url: str,
    prev_version: str = "CURRENT",
) -> str:
    """
    Substitute variables in issue template.

    Args:
        template: Template content
        version: Release version (e.g., "4.46.0")
        commit_sha: Git commit SHA for the release tag
        published_date: ISO date string
        release_notes_url: URL to release notes
        prev_version: Previous version for compare URL (default: "CURRENT")

    Returns:
        Substituted template content

    Raises:
        TemplateError: If substitution fails
    """
    try:
        # Format date
        date = published_date.split("T")[0] if "T" in published_date else published_date

        # Build compare URL
        compare_url = (
            f"https://github.com/gitbucket/gitbucket/compare/{prev_version}...{version}"
        )

        # Perform substitutions
        result = template
        result = result.replace("{VERSION}", version)
        result = result.replace("{COMMIT_SHA}", commit_sha)
        result = result.replace("{PUBLISHED_DATE}", published_date)
        result = result.replace("{RELEASE_NOTES_URL}", release_notes_url)
        result = result.replace("{DATE}", date)
        result = result.replace("{PREV_VERSION}", prev_version)
        result = result.replace("{COMPARE_URL}", compare_url)

        return result

    except Exception as e:
        raise TemplateError(f"Template substitution failed: {e}") from e


def get_tag_commit_sha(token: str, tag: str) -> str:
    """
    Get commit SHA for a git tag.

    Args:
        token: GitHub API token
        tag: Tag name (e.g., "4.46.0")

    Returns:
        Commit SHA or "unknown" if not found
    """
    try:
        url = f"https://api.github.com/repos/gitbucket/gitbucket/git/ref/tags/{tag}"
        data = github_api_get(url, token)
        return data.get("object", {}).get("sha", "unknown")
    except GitHubAPIError:
        logger.warning(f"Could not get commit SHA for tag {tag}")
        return "unknown"


def gh_issue_list(repo: str, labels: list[str], search: str) -> list[dict]:
    """
    List GitHub issues using gh CLI.

    Args:
        repo: Repository (owner/name)
        labels: Labels to filter by
        search: Search query

    Returns:
        List of issue dictionaries

    Raises:
        subprocess.CalledProcessError: If gh command fails
    """
    label_args = ["--label", ",".join(labels)]

    result = subprocess.run(
        [
            "gh",
            "issue",
            "list",
            "--repo",
            repo,
            "--state",
            "open",
            *label_args,
            "--search",
            search,
            "--json",
            "number",
            "--jq",
            ".[].number",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        logger.warning(f"gh issue list failed: {result.stderr}")
        return []

    # Parse output
    output = result.stdout.strip()
    if not output:
        return []

    numbers = []
    for line in output.split("\n"):
        if line.strip():
            try:
                numbers.append({"number": int(line.strip())})
            except ValueError:
                continue

    return numbers


def check_existing_issue(repo: str, version: str) -> Optional[int]:
    """
    Check if an issue already exists for this release.

    Args:
        repo: Repository (owner/name)
        version: Release version to check

    Returns:
        Issue number if exists, None otherwise
    """
    try:
        issues = gh_issue_list(repo, ["upstream", "api-sync"], version)

        if issues:
            issue_num = issues[0]["number"]
            logger.info(f"Issue #{issue_num} already exists for {version}")
            return issue_num

        return None

    except Exception as e:
        logger.warning(f"Failed to check existing issues: {e}")
        return None


def gh_issue_create(repo: str, title: str, body: str, labels: list[str]) -> str:
    """
    Create GitHub issue using gh CLI.

    Args:
        repo: Repository (owner/name)
        title: Issue title
        body: Issue body
        labels: Labels to apply

    Returns:
        Issue URL

    Raises:
        subprocess.CalledProcessError: If gh command fails
    """
    cmd = [
        "gh",
        "issue",
        "create",
        "--repo",
        repo,
        "--title",
        title,
        "--body",
        body,
        "--label",
        ",".join(labels),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd, result.stdout, result.stderr
        )

    return result.stdout.strip()


def create_release_issue(
    token: str,
    repo: str,
    release: dict,
    template: str,
    prev_version: str = "CURRENT",
) -> str:
    """
    Create GitHub issue for a release.

    Args:
        token: GitHub API token
        repo: Target repository (owner/name)
        release: Release dictionary with tag_name, published_at, html_url
        template: Issue template content
        prev_version: Previous version for compare URL

    Returns:
        Issue URL

    Raises:
        subprocess.CalledProcessError: If issue creation fails
    """
    version = release["tag_name"]
    published_date = release["published_at"]
    html_url = release["html_url"]

    # Get commit SHA for the tag
    commit_sha = get_tag_commit_sha(token, version)

    # Substitute template
    body = substitute_template(
        template=template,
        version=version,
        commit_sha=commit_sha,
        published_date=published_date,
        release_notes_url=html_url,
        prev_version=prev_version,
    )

    # Create issue
    title = f"[SPEC] Upstream GitBucket Release {version} - OpenAPI Spec Update"

    issue_url = gh_issue_create(
        repo=repo,
        title=title,
        body=body,
        labels=["api-sync", "upstream", "needs-approval"],
    )

    logger.info(f"Created issue: {issue_url}")
    return issue_url


def process_releases(
    token: str,
    repo: str,
    releases: list[dict],
    template: str,
    dry_run: bool = False,
):
    """
    Process all new releases and create issues.

    Args:
        token: GitHub API token
        repo: Target repository (owner/name)
        releases: List of release dictionaries sorted oldest first
        template: Issue template content
        dry_run: If True, log actions without creating issues
    """
    # Process from oldest to newest
    for i, release in enumerate(releases):
        version = release["tag_name"]

        # Determine previous version for compare URL
        if i == 0:
            # First release - use "CURRENT" placeholder
            prev_version = "CURRENT"
        else:
            # Use previous release version
            prev_version = releases[i - 1]["tag_name"]

        # Check for existing issue
        existing = check_existing_issue(repo, version)
        if existing:
            logger.info(f"Skipping {version} - issue #{existing} already exists")
            continue

        # Create issue
        if dry_run:
            logger.info(
                f"DRY RUN: Would create issue for {version} (compare with {prev_version})"
            )
        else:
            create_release_issue(
                token=token,
                repo=repo,
                release=release,
                template=template,
                prev_version=prev_version,
            )

    logger.info(f"Processing complete. Processed {len(releases)} release(s)")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Detect upstream GitBucket releases and create GitHub issues"
    )
    parser.add_argument(
        "--token",
        required=False,
        default=None,
        help="GitHub API token (default: GITHUB_TOKEN env var)",
    )
    parser.add_argument(
        "--repo",
        required=False,
        default=None,
        help="Target repository (default: GITHUB_REPOSITORY env var)",
    )
    parser.add_argument(
        "--state-file",
        required=False,
        default="workflow-state/last_release.txt",
        help="State file path (default: workflow-state/last_release.txt)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run mode - log actions without creating issues",
    )

    args = parser.parse_args()

    # Get token
    token = args.token or os.environ.get("GITHUB_TOKEN")
    if not token:
        logger.error("GitHub token required (set GITHUB_TOKEN or use --token)")
        sys.exit(1)

    # Get repository
    repo = args.repo or os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        logger.error("Repository required (set GITHUB_REPOSITORY or use --repo)")
        sys.exit(1)

    # Parse repository owner/name
    repo_parts = repo.split("/")
    if len(repo_parts) != 2:
        logger.error(f"Invalid repository format: {repo}")
        sys.exit(1)

    # Resolve paths
    project_root = Path(__file__).resolve().parent.parent
    state_file = project_root / args.state_file
    template_file = project_root / ".github" / "ISSUE_TEMPLATE" / "upstream-release.md"

    logger.info(f"Scanning for releases in {repo}")
    logger.info(f"State file: {state_file}")
    logger.info(f"Template: {template_file}")

    # Read current version
    current_version = read_current_version(state_file)

    # Fetch new releases
    releases = fetch_releases(token, current_version)

    if not releases:
        logger.info("No new releases found")
        sys.exit(0)

    # Load template
    template = load_template(template_file)

    # Process releases
    process_releases(token, repo, releases, template, args.dry_run)

    logger.info("Release detection complete")
    logger.info(
        "Note: State file NOT updated - AI agent will update after processing each release"
    )


if __name__ == "__main__":
    main()
