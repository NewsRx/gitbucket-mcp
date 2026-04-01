# GitBucket Label Operations

## Overview

GitBucket label API is fully functional and auto-creates labels. Source: `ApiIssueLabelControllerBase.scala`.

## Add Labels to Issue

```python
# ✅ CORRECT: POST array of label names
response = requests.post(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues/{issue_number}/labels",
    headers={"Authorization": f"token {token}"},
    json=["enhancement", "bug"]  # ✅ Array format (not objects)
)
# Returns: [{"name": "enhancement", "color": "...", ...}, {"name": "bug", ...}]
```

**Key difference from GitHub**: GitBucket auto-creates labels that don't exist.

## Replace All Labels

```python
# ✅ CORRECT: PUT replaces all labels
response = requests.put(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues/{issue_number}/labels",
    headers={"Authorization": f"token {token}"},
    json=["enhancement", "priority"]  # Replaces all existing labels
)
# Returns: [{"name": "enhancement", ...}, {"name": "priority", ...}]
```

**Behavior**: Removes all existing labels and adds new ones. Auto-creates missing labels.

## Remove Specific Label

```python
# ✅ CORRECT: DELETE specific label
response = requests.delete(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues/{issue_number}/labels/{label_name}",
    headers={"Authorization": f"token {token}"}
)
# Returns: empty response on success
```

**Note**: Label name is in URL path, not body.

## Remove All Labels

```python
# ✅ CORRECT: DELETE all labels (no label name in URL)
response = requests.delete(
    f"{GITBUCKET_URL}api/v3/repos/{owner}/{repo}/issues/{issue_number}/labels",
    headers={"Authorization": f"token {token}"}
)
# Returns: empty response on success
```

## Label Auto-Creation

Unlike GitHub, GitBucket creates labels automatically:

```python
# When adding labels to an issue:
POST /repos/:owner/:repo/issues/:id/labels
["new-label", "another-new-label"]

# GitBucket will:
# 1. Check if "new-label" exists
# 2. Create "new-label" with default color if missing
# 3. Check if "another-new-label" exists
# 4. Create "another-new-label" with default color if missing
# 5. Add both labels to the issue
# 6. Return the label objects
```

**Implication**: No need to pre-create labels before assigning them to issues.

## Direct API vs MCP Tools

| Operation | MCP Tool | Use Direct API |
|-----------|----------|----------------|
| Add labels | ❌ Not available | ✅ POST `/issues/:id/labels` |
| Replace labels | ❌ Not available | ✅ PUT `/issues/:id/labels` |
| Remove label | ❌ Not available | ✅ DELETE `/issues/:id/labels/:name` |
| Remove all labels | ❌ Not available | ✅ DELETE `/issues/:id/labels` |

**Recommendation**: Use direct API calls for label operations.

## Source Code

`ApiIssueLabelControllerBase.scala` shows all endpoints:

```scala
// POST - Add labels to issue (auto-creates missing labels)
post("/api/v3/repos/:owner/:repository/issues/:id/labels")

// PUT - Replace all labels
put("/api/v3/repos/:owner/:repository/issues/:id/labels")

// DELETE - Remove specific label
delete("/api/v3/repos/:owner/:repository/issues/:id/labels/:name")

// DELETE - Remove all labels
delete("/api/v3/repos/:owner/:repository/issues/:id/labels")
```