# AI Agent Quick Reference - GitBucket 4.43.0

**Purpose:** Quick reference for AI agents using GitBucket API endpoints. Condensed from OpenAPI spec with practical usage guidance.

---

## Endpoint Categories

### Repositories

| Endpoint | Method | Required Params | Auth | Notes |
|----------|--------|----------------|------|-------|
| `/repos/{owner}/{repo}` | GET | owner, repo | Optional | Returns repository info |
| `/repos/{owner}/{repo}/branches` | GET | owner, repo | Optional | List branches |
| `/repos/{owner}/{repo}/branches/{branch}` | GET | owner, repo, branch | Optional | Get branch info |
| `/repos/{owner}/{repo}/branches/{branch}/protection` | GET | owner, repo, branch | Required | Branch protection settings |

### Issues

| Endpoint | Method | Required Params | Auth | Notes |
|----------|--------|----------------|------|-------|
| `/repos/{owner}/{repo}/issues` | GET | owner, repo | Optional | List issues (supports `state`, `labels` filters) |
| `/repos/{owner}/{repo}/issues/{issue_number}` | GET | owner, repo, issue_number | Optional | Get issue |
| `/repos/{owner}/{repo}/issues` | POST | owner, repo, title | Required | Create issue (`body`, `labels`, `assignees` optional) |
| `/repos/{owner}/{repo}/issues/{issue_number}` | PATCH | owner, repo, issue_number | Required | Update issue |

### Pull Requests

| Endpoint | Method | Required Params | Auth | Notes |
|----------|--------|----------------|------|-------|
| `/repos/{owner}/{repo}/pulls` | GET | owner, repo | Optional | List PRs (supports `state`, `head`, `base` filters) |
| `/repos/{owner}/{repo}/pulls/{pull_number}` | GET | owner, repo, pull_number | Optional | Get PR details |
| `/repos/{owner}/{repo}/pulls` | POST | owner, repo, title, head, base | Required | Create PR |
| `/repos/{owner}/{repo}/pulls/{pull_number}/merge` | PUT | owner, repo, pull_number | Required | Merge PR |

### Users

| Endpoint | Method | Required Params | Auth | Notes |
|----------|--------|----------------|------|-------|
| `/user` | GET | None | Required | Get authenticated user |
| `/users/{username}` | GET | username | Optional | Get user by username |

### Labels

| Endpoint | Method | Required Params | Auth | Notes |
|----------|--------|----------------|------|-------|
| `/repos/{owner}/{repo}/labels` | GET | owner, repo | Optional | List labels |
| `/repos/{owner}/{repo}/labels/{name}` | GET | owner, repo, name | Optional | Get label by name |
| `/repos/{owner}/{repo}/labels` | POST | owner, repo, name, color | Required | Create label |
| `/repos/{owner}/{repo}/labels/{name}` | DELETE | owner, repo, name | Required | Delete label |

---

## Required Parameters Checklist

### Repository Operations
- **owner**: Repository owner (username or organization)
- **repo**: Repository name

### Issue Operations
- **owner, repo**: (as above)
- **issue_number**: Issue number (integer)
- **title**: Required for creating issues

### Pull Request Operations
- **owner, repo**: (as above)
- **pull_number**: Pull request number (integer)
- **title, head, base**: Required for creating PRs
  - `title`: PR title
  - `head`: Branch containing changes (source)
  - `base`: Branch to merge into (target)

### Label Operations
- **owner, repo**: (as above)
- **name**: Label name
- **color**: 6-digit hex color (with or without `#`)

---

## Known Gotchas

### Authentication
- **Token scope required**: Write operations require `repo` scope or higher
- **Rate limiting**: GitBucket uses headers similar to GitHub:
  - `X-RateLimit-Limit`: Maximum requests per hour
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: UTC timestamp when limit resets

### Issue Numbering
- Issue numbers are repository-scoped (not global)
- Issue numbers start at 1 (not 0)
- Issue numbers are always integers (never strings)

### Pull Request Behavior
- `head` parameter format: `{owner}:{branch}` for cross-repo PRs
- `head` can be just `{branch}` for same-repo PRs
- Merge commits optional (`merge_method` parameter)
- `merge_method` options: `merge`, `squash`, `rebase` (GitBucket may not support all)

### Label Colors
- GitBucket accepts colors with or without `#` prefix
- Example: `ff0000` or `#ff0000` both valid
- API returns colors without `#` prefix

### Sub-issues (Not Supported)
- GitBucket does NOT support native sub-issues (GitHub feature)
- Hierarchical issue linking not available
- Workaround: Use references in issue body

### H2 Database Upgrade (4.43.0 Breaking Change)
- **Backend change only**: No API client changes required
- **H2 users**: MUST migrate database before upgrading
- **PostgreSQL/MySQL users**: No migration required
- **Impact**: API clients unaffected, only GitBucket administrators need migration

---

## Common Usage Patterns

### Creating an Issue

```python
import urllib.request
import json

def create_issue(api_url: str, token: str, owner: str, repo: str, 
                  title: str, body: str = "", labels: list = None, 
                  assignees: list = None) -> dict:
    """Create a new issue in a repository."""
    data = {
        "title": title,
        "body": body,
        "labels": labels or [],
        "assignees": assignees or []
    }
    req = urllib.request.Request(
        f"{api_url}/repos/{owner}/{repo}/issues",
        data=json.dumps(data).encode(),
        headers={
            "Authorization": f"token {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())
```

### Listing Pull Requests with Filters

```python
import urllib.request
import json
from urllib.parse import urlencode

def list_pull_requests(api_url: str, token: str, owner: str, repo: str,
                       state: str = None, head: str = None, base: str = None) -> list:
    """List pull requests with optional filters."""
    params = {}
    if state:
        params["state"] = state
    if head:
        params["head"] = head
    if base:
        params["base"] = base
    
    url = f"{api_url}/repos/{owner}/{repo}/pulls"
    if params:
        url += "?" + urlencode(params)
    
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"token {token}"}
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())
```

### Creating a Pull Request

```python
import urllib.request
import json

def create_pull_request(api_url: str, token: str, owner: str, repo: str,
                        title: str, head: str, base: str, body: str = "") -> dict:
    """Create a new pull request."""
    data = {
        "title": title,
        "head": head,
        "base": base,
        "body": body
    }
    req = urllib.request.Request(
        f"{api_url}/repos/{owner}/{repo}/pulls",
        data=json.dumps(data).encode(),
        headers={
            "Authorization": f"token {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())
```

### Merging a Pull Request

```python
import urllib.request
import json

def merge_pull_request(api_url: str, token: str, owner: str, repo: str,
                       pull_number: int, commit_message: str = None,
                       merge_method: str = "merge") -> dict:
    """Merge a pull request."""
    data = {
        "commit_message": commit_message or f"Merge pull request #{pull_number}",
        "merge_method": merge_method  # 'merge', 'squash', or 'rebase'
    }
    req = urllib.request.Request(
        f"{api_url}/repos/{owner}/{repo}/pulls/{pull_number}/merge",
        data=json.dumps(data).encode(),
        headers={
            "Authorization": f"token {token}",
            "Content-Type": "application/json"
        },
        method="PUT"
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())
```

---

## Version-Specific Notes

### 4.43.0 Changes
- **H2 Database**: Upgraded from 1.x to 2.x (backend only, no API impact)
- **API Endpoints**: No changes - all 93 endpoints remain compatible
- **API Controllers**: Whitespace formatting only (no functional changes)
- **Schema**: No changes to request/response schemas

### 4.43.0 Breaking Change (H2 Users Only)

**⚠️ If your GitBucket instance uses H2 database:**

Before upgrading to 4.43.0, you MUST migrate:

```bash
# 1. Export with H2 1.4.199
curl -O https://repo1.maven.org/maven2/com/h2database/h2/1.4.199/h2-1.4.199.jar
java -cp h2-1.4.199.jar org.h2.tools.Script \
    -url "jdbc:h2:~/.gitbucket/data" \
    -user sa -password sa \
    -script dump.sql

# 2. Remove old database
rm -rf ~/.gitbucket/data*

# 3. Import with H2 2.3.232
curl -O https://repo1.maven.org/maven2/com/h2database/h2/2.3.232/h2-2.3.232.jar
java -cp h2-2.3.232.jar org.h2.tools.RunScript \
    -url "jdbc:h2:~/.gitbucket/data" \
    -user sa -password sa \
    -script dump.sql

# 4. Update database.conf if needed (remove MVCC=true)
```

**If using PostgreSQL or MySQL:** No migration required, upgrade directly.

### Compatibility
- Clients designed for GitHub API may require adjustments
- Some GitHub-specific features (draft PRs, sub-issues) not available
- Rate limits differ from GitHub

---

## Source Code Gotchas (From Code Analysis)

### Code Comments Identified (4.43.0)

**API Controllers:**
- No significant code comments in this version
- Whitespace formatting changes only

**Service Layer:**
- Internal implementation changes (no API impact)
- H2 upgrade affects database layer only

**General:**
- All API endpoints remain compatible with 4.42.1
- No schema changes required for API clients

---

## Total Endpoints

| Version | Count | Notes |
|---------|-------|-------|
| 4.42.1 | 93 | Baseline |
| 4.43.0 | 93 | No change |

---

## References

- **OpenAPI Spec**: `openapi.json` in this directory
- **API Diff**: `api-diff.md` in this directory
- **Release Notes**: `release-notes.md` in this directory
- **Upstream**: https://github.com/gitbucket/gitbucket
- **API Version**: GitHub REST API v3 (compatible subset)

---

🤖 Generated from OpenAPI spec analysis for AI agent consumption