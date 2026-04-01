---
name: gitbucket-api
description: GitBucket API patterns and capabilities. Documents GitHub-compatible API, correct authentication, and working patterns for issues, labels, and comments based on source code analysis.
license: MIT
compatibility: opencode
---

# GitBucket API Skill

## Role

You are a GitBucket API specialist focused on correct API usage patterns and error recovery.

## Overview

GitBucket implements a GitHub-compatible API v3. Most operations work as documented in GitHub's API, with some important differences around authentication and error handling.

## When to Use

Invoke this skill when:
- Working with GitBucket repositories (detected from remote URL)
- Creating/updating GitBucket issues
- Managing labels on GitBucket issues
- Debugging GitBucket API failures ("Bad credentials")

## API Compatibility Matrix

| Operation | GitHub API | GitBucket API | Status |
|-----------|------------|---------------|--------|
| Token auth GET/POST | ✅ Works | ✅ Works | Use token for all operations |
| Token auth PATCH/PUT/DELETE | ✅ Works | ✅ Works | Works correctly |
| Basic auth | ✅ Works | ❌ "Bad credentials" | Token only |
| Create issue with labels | ✅ Works | ✅ Works | Labels in create call |
| Add labels to issue | ✅ Works | ✅ Works | POST `/issues/:id/labels` |
| Replace all labels | ✅ Works | ✅ Works | PUT `/issues/:id/labels` |
| Remove label from issue | ✅ Works | ✅ Works | DELETE `/issues/:id/labels/:name` |
| Remove all labels | ✅ Works | ✅ Works | DELETE `/issues/:id/labels` |
| Auto-create missing labels | ❌ Fails | ✅ Works | GitBucket creates labels automatically |

## Authentication

### ✅ CORRECT: Token Authentication Only

GitBucket requires token authentication. Basic auth does NOT work.

```python
# Session init provides these values:
GITBUCKET_URL = os.environ.get("GITBUCKET_URL")
GITBUCKET_TOKEN = os.environ.get("GITBUCKET_TOKEN")

# Use token in Authorization header:
headers = {
    "Authorization": f"token {GITBUCKET_TOKEN}",
    "Content-Type": "application/json",
}
```

### 🚫 FORBIDDEN: Basic Authentication

```python
# WRONG: Basic auth fails with "Bad credentials"
import base64
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
headers = {"Authorization": f"Basic {credentials}"}  # ❌ WILL FAIL
```

## Issue Operations

See `tasks/issue-operations.md` for detailed patterns.

### Create Issue

```python
# ✅ CORRECT: Create issue with token auth and labels
response = requests.post(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues",
    headers={"Authorization": f"token {token}"},
    json={
        "title": "Issue title",
        "body": "Issue body",
        "labels": ["label-name"],  # ✅ Works - labels appear immediately
        "assignees": ["username"],  # ✅ Works
        "milestone": 5,  # ✅ Works
    }
)
# Returns: {"number": 123, "id": 456789, ...}
```

### Get Issue

```python
# ✅ CORRECT: Read issue
response = requests.get(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues/{issue_number}",
    headers={"Authorization": f"token {token}"}
)
```

### Update Issue

```python
# ✅ CORRECT: Update any field via PATCH
response = requests.patch(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues/{issue_number}",
    headers={"Authorization": f"token {token}"},
    json={
        "title": "New title",
        "body": "New body",
        "state": "open",  # or "closed"
        "labels": ["enhancement", "bug"],  # ✅ Works - updates labels
    }
)
```

## Label Operations

See `tasks/label-operations.md` for detailed patterns.

### Add Labels to Existing Issue

```python
# ✅ CORRECT: POST array of label names
response = requests.post(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues/{issue_number}/labels",
    headers={"Authorization": f"token {token}"},
    json=["enhancement", "bug"]  # ✅ Array format works
)
# Returns: [{"name": "enhancement", ...}, {"name": "bug", ...}]
```

### Replace All Labels on Issue

```python
# ✅ CORRECT: PUT replaces all labels
response = requests.put(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues/{issue_number}/labels",
    headers={"Authorization": f"token {token}"},
    json=["enhancement", "priority"]  # Replaces all existing labels
)
```

### Remove Specific Label from Issue

```python
# ✅ CORRECT: DELETE specific label
response = requests.delete(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues/{issue_number}/labels/{label_name}",
    headers={"Authorization": f"token {token}"}
)
```

### Remove All Labels from Issue

```python
# ✅ CORRECT: DELETE all labels
response = requests.delete(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues/{issue_number}/labels",
    headers={"Authorization": f"token {token}"}
)
```

## Label Auto-Creation Behavior

GitBucket automatically creates labels that don't exist:

```python
# When adding labels to an issue:
POST /repos/:owner/:repo/issues/:id/labels
["new-label", "another-new-label"]

# GitBucket will:
# 1. Create "new-label" if it doesn't exist (with default color)
# 2. Create "another-new-label" if it doesn't exist
# 3. Add both labels to the issue
# 4. Return the label objects
```

This is different from GitHub's API which requires labels to exist first.

## Error Recovery

See `tasks/error-recovery.md` for detailed procedures.

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Bad credentials" | Basic auth attempted | Use token authentication only |
| "Not Found" | Wrong endpoint URL | Verify URL format: `/api/v3/repos/{owner}/{repo}/...` |
| "Unauthorized" | Token missing or invalid | Check `GITBUCKET_TOKEN` value |
| 422 Unprocessable Entity | Label already exists | GitBucket returns validation error for duplicate labels |

## Session Init Integration

Session init (`ai_bin/session_init.py`) detects GitBucket and outputs:

```
GIT_PLATFORM=gitbucket
GITBUCKET_URL=https://gitbucket.example.com/gitbucket/
GITBUCKET_HAS_CREDENTIALS=true
```

## Tool Selection

| Operation | Use This Tool |
|-----------|---------------|
| Create issue | `gitbucket_create_issue` (MCP) |
| Get issue | `gitbucket_get_issue` (MCP) |
| Update issue | `gitbucket_update_issue` (MCP) |
| List issues | `gitbucket_list_issues` (MCP) |
| Add comment | `gitbucket_add_issue_comment` (MCP) |
| Add labels | Direct API POST (MCP doesn't have label tools) |

## Source Code Reference

This skill is based on analysis of GitBucket source code:
- `ApiIssueControllerBase.scala` - Issue endpoints
- `ApiIssueLabelControllerBase.scala` - Label endpoints
- `CreateAnIssue.scala` - Create issue model
- `AddLabelsToAnIssue.scala` - Add labels model

## Sub-Tasks

- `tasks/issue-operations.md` - Issue CRUD patterns
- `tasks/label-operations.md` - Label CRUD patterns
- `tasks/error-recovery.md` - Error handling

## Guidelines Reference

| Guideline | Section |
|-----------|---------|
| `000-session-init.md` | GitBucket detection and credentials |
| `122-github-mcp-operations.md` | GitBucket-specific notes |