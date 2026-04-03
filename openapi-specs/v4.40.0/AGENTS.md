# GitBucket API Quick Reference - v4.40.0

**Version:** 4.40.0  
**Release Notes:** https://github.com/gitbucket/gitbucket/releases/tag/4.40.0

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

### ✅ Baseline Version

This version is the **baseline** for API documentation. No known gotchas at this level.

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

### Create Pull Request

```python
import urllib.request
import json

def create_pull_request(api_url: str, token: str, owner: str, repo: str, 
                        title: str, head: str, base: str) -> dict:
    data = json.dumps({"title": title, "head": head, "base": base}).encode()
    req = urllib.request.Request(
        f"{api_url}/repos/{owner}/{repo}/pulls",
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
    """Baseline version - returns simple string array"""
    req = urllib.request.Request(
        f"{api_url}/repos/{owner}/{repo}/tags",
        headers={"Authorization": f"token {token}"}
    )
    with urllib.request.urlopen(req) as response:
        tags = json.loads(response.read().decode())
    
    # v4.41.0 and earlier: ["tag1", "tag2", "tag3"]
    # v4.42.0+: [{"name": "tag1", ...}, {"name": "tag2", ...}]
    return tags
```

---

## Version-Specific Notes

### v4.40.0

- **Stable baseline:** This is the reference version for API compatibility
- **No known issues:** Baseline for all api-diff comparisons

### Future Compatibility Notes

- **v4.42.0** will change tags endpoint from string array to structured objects
- **v4.42.1** has internal API signature change (no external impact)
- **v4.43.0** introduces H2 database migration

---

## Source Code Gotchas

### TODO/FIXME Markers in Code

| Marker | File | Description |
|--------|------|-------------|
| - | Baseline version - reference only | - |

---

## Related Versions

- **Next:** v4.41.0 - No API changes
- **Future:** v4.42.0 - **BREAKING:** Tags endpoint schema change

---

*Quick reference for AI agents working with GitBucket API - v4.40.0 (Baseline)*