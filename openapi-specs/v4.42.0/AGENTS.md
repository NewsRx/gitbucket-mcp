# GitBucket API Quick Reference - v4.42.0

**Version:** 4.42.0  
**Release Date:** 2025-01-XX  
**GitBucket Tag:** 572f83327fe2970747bd88eae95161e6af7519cc  
**Release Notes:** https://github.com/gitbucket/gitbucket/releases/tag/4.42.0

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

### ⚠️ CRITICAL: Tags Endpoint Breaking Change

**Endpoint:** `GET /api/v3/repos/{owner}/{repo}/tags`

**Old Response (v4.41.0):**
```json
["tag1", "tag2", "tag3"]
```

**New Response (v4.42.0):**
```json
[
  {
    "name": "tag1",
    "commit": {
      "sha": "abc123",
      "url": "/owner/repo/commits/abc123"
    },
    "zipball_url": "/owner/repo/archive/tag1.zip",
    "tarball_url": "/owner/repo/archive/tag1.tar.gz"
  }
]
```

**Impact:**
- **BREAKING:** Code expecting string arrays will fail
- **BREAKING:** Tests mocking tags endpoint with string arrays will fail
- **BREAKING:** Type definitions assuming `string[]` need update

**Migration Required:** See Migration Guide section below.

### ⚠️ Branch Name Length Increased

- **Old limit:** 100 characters
- **New limit:** 255 characters

**Impact:** Branch names up to 255 characters now supported. Update clients that validate branch name length.

### ✅ ssh_url Field Now Populated

- **Old (v4.41.0):** `ssh_url` was empty string
- **New (v4.42.0):** `ssh_url` contains `/owner/repo.git` path

**Impact:** Clients can now rely on `ssh_url` being populated. No breaking change - code expecting empty string still works.

### ⚠️ Java 17 Required

- **Old:** Java 11+ supported
- **New:** Java 17+ required (Scala 3 dependency)

**Impact:** Server deployment only. **No API client impact.**

---

## Required Parameters Checklist

### Repository Endpoints

| Endpoint | Required Params | Notes |
|----------|-----------------|-------|
| `GET /repos/{owner}/{repo}` | `owner`, `repo` | - |
| `GET /repos/{owner}/{repo}/branches` | `owner`, `repo` | List branches |
| `GET /repos/{owner}/{repo}/branches/{branch}` | `owner`, `repo`, `branch` | Get branch |
| `GET /repos/{owner}/{repo}/tags` | `owner`, `repo` | **BREAKING:** Returns `ApiTag[]` not `string[]` |
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

### Tags Endpoint (v4.42.0+)

```python
import urllib.request
import json

def get_tags(api_url: str, token: str, owner: str, repo: str) -> list:
    """Get tags - returns structured ApiTag objects since v4.42.0"""
    req = urllib.request.Request(
        f"{api_url}/repos/{owner}/{repo}/tags",
        headers={"Authorization": f"token {token}"}
    )
    with urllib.request.urlopen(req) as response:
        tags = json.loads(response.read().decode())
    
    # Response: [{"name": "v1.0.0", "commit": {"sha": "...", "url": "..."}, "zipball_url": "..."}]
    
    # Extract tag names (migration required from v4.41.0 string arrays)
    tag_names = [tag['name'] for tag in tags]
    return tags  # Returns list of ApiTag objects
```

---

## Version-Specific Notes

### v4.42.0 Breaking Changes

| Change | Impact | Migration Required |
|--------|--------|-------------------|
| Tags endpoint schema | **BREAKING** | Yes - see Migration Guide |
| Branch name limit 255 | Low | Update validators |
| ssh_url populated | Low | Optional - now usable |
| Java 17 required | Server only | Deployment only |

---

## Migration Guide

### ⚠️ Tags Endpoint Migration (CRITICAL)

**Before (v4.41.0):**
```python
# Simple string array response
tags = api.get("/repos/owner/repo/tags")
for tag in tags:
    # tag is a string
    print(f"Tag: {tag}")  # "tag1", "tag2", etc.
```

**After (v4.42.0):**
```python
# Structured ApiTag objects response
tags = api.get("/repos/owner/repo/tags")
for tag in tags:
    # tag is now an object with fields
    print(f"Tag: {tag['name']}")  # Extract name from object
    print(f"  Commit: {tag['commit']['sha']}")
    print(f"  Archive: {tag['zipball_url']}")
```

**Type Definitions:**

```typescript
// Before (v4.41.0)
type TagsResponse = string[];

// After (v4.42.0)
interface ApiTag {
  name: string;
  commit: {
    sha: string;
    url: string;
  };
  zipball_url: string;
  tarball_url: string;
}
type TagsResponse = ApiTag[];
```

### Branch Name Length Migration

```python
# Before (v4.41.0)
if len(branch_name) > 100:
    raise ValueError("Branch name too long")

# After (v4.42.0)
if len(branch_name) > 255:
    raise ValueError("Branch name too long")
```

---

## Source Code Gotchas

### TODO/FIXME Markers in Code

| Marker | File | Description |
|--------|------|-------------|
| - | No critical markers in v4.42.0 | - |

---

## Related Versions

- **Previous:** v4.41.0 - No API changes
- **Next:** v4.42.1 - Internal API signature change (no external impact)

---

*Quick reference for AI agents working with GitBucket API - v4.42.0*