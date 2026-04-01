# GitBucket Issue Operations

## Overview

Issue CRUD operations use GitHub-compatible endpoints with token authentication.

## Create Issue

```python
# ✅ CORRECT: Create issue with all supported fields
response = requests.post(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues",
    headers={"Authorization": f"token {token}"},
    json={
        "title": "Issue title",
        "body": "Issue body",
        "labels": ["enhancement", "bug"],  # ✅ Auto-creates labels
        "assignees": ["username"],  # ✅ Works
        "milestone": 5,  # ✅ Works - milestone number
    }
)
```

**Fields supported** (from `CreateAnIssue.scala`):
- `title` (required) - Issue title
- `body` (optional) - Issue description
- `labels` (optional) - Array of label names
- `assignees` (optional) - Array of usernames
- `milestone` (optional) - Milestone number

**Response**: Issue object with `number`, `id`, `state`, etc.

## Get Issue

```python
# ✅ CORRECT: Read issue by number
response = requests.get(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues/{issue_number}",
    headers={"Authorization": f"token {token}"}
)
```

## Update Issue

```python
# ✅ CORRECT: Update any field via PATCH
response = requests.patch(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues/{issue_number}",
    headers={"Authorization": f"token {token}"},
    json={
        "title": "New title",
        "body": "New body",
        "state": "closed",  # Close issue
        "labels": ["enhancement"],  # Replace labels
    }
)
```

**Note**: GitBucket closing issues via REST API may not work on some instances. The MCP tool returned error: "This GitBucket instance does not support REST issue updates".

## List Issues

```python
# ✅ CORRECT: List repository issues
response = requests.get(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues",
    headers={"Authorization": f"token {token}"},
    params={
        "state": "open",  # or "closed" or "all"
        "labels": "bug,enhancement",  # Filter by labels
    }
)
```

## Add Comment

```python
# ✅ CORRECT: Add comment to issue
response = requests.post(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues/{issue_number}/comments",
    headers={"Authorization": f"token {token}"},
    json={"body": "Comment text"}
)
```

## Tool Selection

| Operation | Use MCP Tool |
|-----------|--------------|
| Create issue | `gitbucket_create_issue` |
| Get issue | `gitbucket_get_issue` |
| Update issue | `gitbucket_update_issue` |
| List issues | `gitbucket_list_issues` |
| Add comment | `gitbucket_add_issue_comment` |

## Source Code

- `ApiIssueControllerBase.scala` - Issue endpoints implementation
- `CreateAnIssue.scala` - Create issue model
- `ApiIssue.scala` - Issue response model