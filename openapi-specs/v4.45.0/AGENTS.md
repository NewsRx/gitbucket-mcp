# AI Agent Quick Reference - GitBucket 4.45.0

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

### Branch Protection API (Since 4.44.0)
- **Schema**: Response uses `ApiBranchProtectionResponse` type
- **Fields**: `enforce_admins` (boolean), `restrictions` (array)
- **Migration**: Clients expecting pre-4.44.0 schema need update

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

### Adding Labels to Repository

```python
import urllib.request
import json

def create_label(api_url: str, token: str, owner: str, repo: str,
                  name: str, color: str, description: str = "") -> dict:
    """Create a new label in a repository."""
    data = {
        "name": name,
        "color": color.lstrip("#"),  # Remove # if present
        "description": description
    }
    req = urllib.request.Request(
        f"{api_url}/repos/{owner}/{repo}/labels",
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

---

## Source Code Gotchas (From Code Analysis)

### Code Comments Identified (Pre-existing, Not New in 4.45.0)

**Issue Milestone Controller** (`ApiIssueMilestoneControllerBase.scala`):
- `// TODO "sort", "direction" params should be implemented.` - Sorting params not implemented

**Repository Collaborator Controller** (`ApiRepositoryCollaboratorControllerBase.scala`):
- `// TODO Should ApiUser take permission?` - Permission field may be missing

**Pull Request Controller** (`ApiPullRequestControllerBase.scala`):
- `// TODO: more api spec condition` - Not all GitHub API conditions implemented
- `// TODO: crash when body is empty` - Empty body may cause errors
- `// TODO: Implement sha parameter` - SHA parameter not supported
- `// TODO: Implement commit_title` - Commit title not customizable

**Issue Label Controller** (`ApiIssueLabelControllerBase.scala`):
- `// TODO ApiError should support errors field` - Error responses may lack detail

**Issue Controller** (`ApiIssueControllerBase.scala`):
- `// TODO: more api spec condition` - Not all GitHub API conditions implemented

**API Models** (various):
- `MergeAPullRequest.scala`: `/* TODO: Not Implemented */` - Comment field in PR merge
- `ApiCommits.scala`: `comment_url` always empty (no API for commit comments)
- `ApiPullRequest.scala`: `mergeable` is always None (not checked)

---

## Version-Specific Notes

### 4.45.0 (Current)
- **No API changes** from 4.44.0
- UI-only release: full username display, render plugin support, wiki link syntax
- All API endpoints remain identical

### 4.44.0
- **Branch Protection**: Schema changed, new fields added
- **New endpoint**: Branch protection enforcement for admins
- **Breaking change**: Old clients may fail on branch protection response

### Compatibility
- Clients designed for GitHub API may require adjustments
- Some GitHub-specific features (draft PRs, sub-issues) not available
- Rate limits differ from GitHub

---

## References

- **OpenAPI Spec**: `openapi.json` in this directory
- **API Diff**: `api-diff.md` in this directory
- **Upstream**: https://github.com/gitbucket/gitbucket
- **API Version**: GitHub REST API v3 (compatible subset)

---

🤖 Generated from OpenAPI spec analysis for AI agent consumption