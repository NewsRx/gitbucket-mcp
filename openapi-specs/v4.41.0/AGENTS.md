# GitBucket API Quick Reference - v4.41.0

**Version:** 4.41.0  
**Release Date:** 2024-05-18  
**Commit SHA:** 598f28931136f14eb897dac30fe0707efaab2adf  
**Release Notes:** https://github.com/gitbucket/gitbucket/releases/tag/4.41.0

---

## Endpoint Categories

| Category | Endpoints | Notes |
|----------|-----------|-------|
| Repository | 15+ | repos, branches, tags, commits |
| Issues | 12+ | issues, comments, labels |
| Pull Requests | 10+ | PRs, reviews, comments |
| Users | 5+ | user info, authentication |
| Organizations | 8+ | orgs, teams, members |
| Webhooks | 6+ | webhook CRUD and delivery |

---

## Known Gotchas

### ✅ No Breaking Changes

This version has **no breaking API changes** from v4.40.0.

### Performance Improvements

- **Branch listing:** `GET /repos/{owner}/{repo}/branches` endpoint has improved performance for repositories with many branches

### Library Upgrades

- Scalatra 3.0.0
- JGit 6.9.0
- Various security updates

**Impact:** Internal only - no API client changes needed.

---

## Required Parameters Checklist

### Repository Endpoints

| Endpoint | Required Params | Notes |
|----------|-----------------|-------|
| `GET /repos/{owner}/{repo}` | `owner`, `repo` | - |
| `GET /repos/{owner}/{repo}/branches` | `owner`, `repo` | List branches |
| `GET /repos/{owner}/{repo}/branches/{branch}` | `owner`, `repo`, `branch` | Get branch |
| `GET /repos/{owner}/{repo}/tags` | `owner`, `repo` | Returns `string[]` (array of strings) |
| `GET /repos/{owner}/{repo}/commits` | `owner`, `repo` | Optional `sha`, `path`, `page` |
| `POST /repos/{owner}/{repo}/forks` | `owner`, `repo` | Fork repository |

### Issue Endpoints

| Endpoint | Required Params | Notes |
|----------|-----------------|-------|
| `GET /repos/{owner}/{repo}/issues` | `owner`, `repo` | Optional `state`, `labels`, `sort` |
| `POST /repos/{owner}/{repo}/issues` | `owner`, `repo`, `title` | Body, labels optional |
| `PATCH /repos/{owner}/{repo}/issues/{number}` | `owner`, `repo`, `number` | Update issue |
| `GET /repos/{owner}/{repo}/issues/{number}/comments` | `owner`, `repo`, `number` | List comments |

### Pull Request Endpoints

| Endpoint | Required Params | Notes |
|----------|-----------------|-------|
| `GET /repos/{owner}/{repo}/pulls` | `owner`, `repo` | Optional `state`, `head`, `base` |
| `POST /repos/{owner}/{repo}/pulls` | `owner`, `repo`, `title`, `head`, `base` | Create PR |
| `GET /repos/{owner}/{repo}/pulls/{number}` | `owner`, `repo`, `number` | Get PR details |

### Authentication

| Endpoint | Required Params | Notes |
|----------|-----------------|-------|
| `POST /session` | - | Uses Basic Auth header |
| `GET /user` | - | Get authenticated user |

---

## Common Usage Patterns

### Authentication

```python
import urllib.request
import urllib.error
import base64
import json

# Personal access token (recommended)
def get_user_with_token(api_url: str, token: str) -> dict:
    req = urllib.request.Request(
        f"{api_url}/user",
        headers={"Authorization": f"token {token}"}
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

# Basic authentication (also supported)
def get_user_with_basic(api_url: str, username: str, password: str) -> dict:
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    req = urllib.request.Request(
        f"{api_url}/user",
        headers={"Authorization": f"Basic {credentials}"}
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())
```

### Pagination

```python
import urllib.request
import json

def list_issues(api_url: str, token: str, owner: str, repo: str, page: int = 1, per_page: int = 100) -> list:
    req = urllib.request.Request(
        f"{api_url}/repos/{owner}/{repo}/issues?page={page}&per_page={per_page}",
        headers={"Authorization": f"token {token}"}
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())
```

### Create Issue

```python
import urllib.request
import json

def create_issue(api_url: str, token: str, owner: str, repo: str, title: str, body: str = "") -> dict:
    data = json.dumps({"title": title, "body": body}).encode()
    req = urllib.request.Request(
        f"{api_url}/repos/{owner}/{repo}/issues",
        data=data,
        headers={
            "Authorization": f"token {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())
```

### Tags Endpoint

```python
import urllib.request
import json

def get_tags(api_url: str, token: str, owner: str, repo: str) -> list:
    """Get tags - returns simple string array in v4.41.0
    
    NOTE: v4.42.0 changes this to structured ApiTag objects!
    Migration required when upgrading to v4.42.0+
    """
    req = urllib.request.Request(
        f"{api_url}/repos/{owner}/{repo}/tags",
        headers={"Authorization": f"token {token}"}
    )
    with urllib.request.urlopen(req) as response:
        tags = json.loads(response.read().decode())
    
    # v4.41.0 Response: ["tag1", "tag2", "tag3"]
    # v4.42.0 will return: [{"name": "tag1", ...}, {"name": "tag2", ...}]
    return tags  # Simple string array in v4.41.0
```

---

## Version-Specific Notes

### v4.41.0

- **Stable API:** No breaking changes from v4.40.0
- **Performance:** Branch listing performance improved
- **Keyword Search:** Web UI feature only - no API changes

### Tags Endpoint Behavior

This version returns tags as **simple string arrays**. **v4.42.0 changes this to structured objects** - plan migration if upgrading.

```python
# v4.41.0 response format
tags = ["v1.0.0", "v1.1.0", "v2.0.0"]

# v4.42.0 will require migration to:
# [{"name": "v1.0.0", ...}, {"name": "v1.1.0", ...}, ...]
```

---

## Source Code Gotchas

### TODO/FIXME Markers in Code

| Marker | File | Description |
|--------|------|-------------|
| - | No critical markers in v4.41.0 | - |

---

## Related Versions

- **Previous:** v4.40.0 - Baseline (no API changes)
- **Next:** v4.42.0 - **BREAKING:** Tags endpoint schema change

---

*Quick reference for AI agents working with GitBucket API - v4.41.0*