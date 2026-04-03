# GitBucket API Quick Reference - v4.42.1

**Version:** 4.42.1  
**Release Date:** 2025-01-20  
**Release Notes:** https://github.com/gitbucket/gitbucket/releases/tag/4.42.1

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

### ⚠️ CRITICAL: Internal API Breaking Change (NOT IN CHANGELOG)

**Function Signature Changed:** `getBranchesNoMergeInfo(git, defaultBranch)` → `getBranchesNoMergeInfo(git)`

- **File:** `src/main/scala/gitbucket/core/util/JGitUtil.scala`
- **4.42.0:** `def getBranchesNoMergeInfo(git: Git, defaultBranch: String): Seq[BranchInfoSimple]`
- **4.42.1:** `def getBranchesNoMergeInfo(git: Git): Seq[BranchInfoSimple]`

**Impact:**
- **External API clients:** No impact - REST API endpoints remain compatible
- **Custom plugins:** Must update function calls to remove `defaultBranch` parameter

**Plugin Migration:**
```scala
// Before (4.42.0)
val branches = JGitUtil.getBranchesNoMergeInfo(git, repository.defaultBranch)

// After (4.42.1)
val branches = JGitUtil.getBranchesNoMergeInfo(git)
```

### ⚠️ CHANGELOG Was Wrong

The CHANGELOG stated only "Fix LDAP issue with SSL" but source code analysis revealed:
- LDAP SSL fix (correct)
- Internal API signature change (NOT documented)
- Multiple controller updates (NOT documented)

---

## Required Parameters Checklist

### Repository Endpoints

| Endpoint | Required Params | Notes |
|----------|-----------------|-------|
| `GET /repos/{owner}/{repo}` | `owner`, `repo` | - |
| `GET /repos/{owner}/{repo}/branches` | `owner`, `repo` | List branches |
| `GET /repos/{owner}/{repo}/branches/{branch}` | `owner`, `repo`, `branch` | Get branch |
| `GET /repos/{owner}/{repo}/tags` | `owner`, `repo` | Returns `ApiTag[]` since 4.42.0 |
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

---

## Version-Specific Notes

### v4.42.1

- **LDAP SSL Fix:** Resolved LDAP authentication issue with SSL connections (server-side only)
- **Internal Change:** Default branch detection logic changed - now handled internally instead of explicit parameter

### Migration from 4.42.0

- **External API clients:** No changes needed
- **Custom plugins:** Update `getBranchesNoMergeInfo()` calls to remove `defaultBranch` parameter

---

## Source Code Gotchas

### TODO/FIXME Markers in Code

| Marker | File | Description |
|--------|------|-------------|
| - | No critical markers found | - |

---

## Related Versions

- **Previous:** v4.42.0 - Tags endpoint breaking change (string array → ApiTag objects)
- **Next:** v4.43.0 - H2 database migration

---

*Quick reference for AI agents working with GitBucket API - v4.42.1*