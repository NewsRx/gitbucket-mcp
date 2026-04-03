# AI Agent Quick Reference - GitBucket 4.44.0

**Purpose:** Quick reference for AI agents using GitBucket API endpoints. Condensed from OpenAPI spec with practical usage guidance.

---

## Endpoint Categories

### Repositories

| Endpoint | Method | Required Params | Auth | Notes |
|----------|--------|----------------|------|-------|
| `/repos/{owner}/{repo}` | GET | owner, repo | Optional | Returns repository info |
| `/repos/{owner}/{repo}/branches` | GET | owner, repo | Optional | List branches |
| `/repos/{owner}/{repo}/branches/{branch}` | GET | owner, repo, branch | Optional | Get branch info |
| `/repos/{owner}/{repo}/branches/{branch}/protection` | GET | owner, repo, branch | Required | ⚠️ **Schema changed in 4.44.0** |

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

### Branch Protection API (Breaking Change in 4.44.0)
- **Schema changed**: Response type changed from `ApiBranchProtection` to `ApiBranchProtectionResponse`
- **New field**: `enforce_admins` added (boolean)
- **New field**: `restrictions` array for allowed users
- **Migration**: Clients expecting `ApiBranchProtection` schema will break
- **Impact**: Any code deserializing branch protection responses needs schema update

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

## Branch Protection (4.44.0+)

### New Schema Fields

```json
{
  "url": "string",
  "enabled": true,
  "required_status_checks": {
    "url": "string",
    "enforcement_level": "off|non_admins|everyone",
    "contexts": ["string"],
    "contexts_url": "string"
  },
  "enforce_admins": true,
  "restrictions": {
    "users": ["username"],
    "teams": ["teamname"]
  }
}
```

### ⚠️ Breaking Change Notice

Clients expecting the old `ApiBranchProtection` schema need to update to `ApiBranchProtectionResponse`:

- **Old**: Response directly returned protection settings
- **New**: Response wrapped with additional metadata
- **Migration**: Update response deserialization to handle new schema

---

## Source Code Gotchas (From Code Analysis)

### Code Comments Identified

**Branch Protection Controller** (`ApiBranchProtectionController.scala`):
- `// TODO: Add support for required status checks` - Status checks not fully implemented
- `// FIXME: Team restrictions not validated` - Team restrictions may not work as expected
- `// NOTE: enforce_admins applies to repository admins` - Admins are NOT exempt by default

**Issues Controller** (`ApiIssuesController.scala`):
- `// NOTE: Issue numbers are repository-scoped` - Not global
- `// WARNING: Large issue bodies may be truncated` - Body size limits exist

**Pull Requests Controller** (`ApiPullRequestsController.scala`):
- `// TODO: Support draft PRs` - Draft PRs not yet implemented
- `// NOTE: merge_method defaults to 'merge'` - Default merge strategy

**General**:
- GitBucket implements GitHub API v3 but may not support all endpoints
- Rate limiting is less aggressive than GitHub (higher limits)
- Authentication tokens can be personal access tokens or OAuth tokens

---

## Version-Specific Notes

### 4.44.0 Changes
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
- **Release Notes**: `release-notes.md` in this directory
- **Upstream**: https://github.com/gitbucket/gitbucket
- **API Version**: GitHub REST API v3 (compatible subset)

---

🤖 Generated from OpenAPI spec analysis for AI agent consumption