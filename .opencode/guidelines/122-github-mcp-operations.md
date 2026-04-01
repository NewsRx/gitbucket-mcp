# GitHub Workflow: MCP Operations

## Tool Preference Summary

| Operation | GitHub MCP Available | GitHub MCP Unavailable |
|-----------|----------------------|--------------------------|
| Spec tracking | GitHub Issues | GitHub Issues via `gh` CLI |
| Create spec | `github_issue_write` | `gh issue create` |
| Track progress | Issue body STATUS + labels | Issue body STATUS + labels |
| Archive | Close issue (no file needed) | Close issue via `gh` CLI |
| Create PR | `github_create_pull_request` | `gh pr create` |
| Merge PR | 🚫 **NEVER — human only** | 🚫 **NEVER — human only** |
| Review | `github_request_copilot_review` | `gh pr review` |

---

## GitHub MCP Coverage

The GitHub MCP tools cover ALL repository operations:

| Category | Operations |
|----------|------------|
| **Issues** | read, write, create, update, label, comment, sub-issues |
| **Pull requests** | read, create, merge (human approval required), review, comment |
| **Repositories** | branches, commits, files, releases, tags, forking |
| **Search** | code, issues, PRs, repos, users |
| **Teams** | members, teams |

**Use GitHub MCP tools INSTEAD OF:**
- Opening browser to GitHub UI
- Using `gh` CLI for operations covered by MCP
- Manual API calls via curl
- Direct file operations on repository files

---

## Permissions Reference

| Tool | Required Permission |
|------|---------------------|
| `github_issue_read` | `issues: read` |
| `github_issue_write` | `issues: write` |
| `github_create_pull_request` | `pull_requests: write` |
| `github_pull_request_read` | `pull_requests: read` |
| `github_merge_pull_request` | `pull_requests: write` (PROHIBITED by guidelines) |
| `github_get_file_contents` | `contents: read` |
| `github_push_files` | `contents: write` |

---

## GitBucket API Differences

When working with GitBucket repositories, use the `gitbucket_api` skill for GitBucket-specific patterns.

### Platform Detection

Session init (`ai_bin/session_init.py`) detects GitBucket from remote URL:

```
GIT_PLATFORM=gitbucket
GITBUCKET_URL=https://gitbucket.example.com/gitbucket/
GITBUCKET_HAS_CREDENTIALS=true
```

### Key Differences from GitHub

| Operation | GitHub | GitBucket | Correct Pattern |
|-----------|--------|-----------|-----------------|
| Authentication | Basic or token | Token only | Use `Authorization: token {TOKEN}` |
| PATCH with labels | Works | Fails | Include title/body/state, or create with labels |
| Label operations | POST array works | Returns 200 but may not persist | Test object format, create with labels |

### GitBucket-Specific Tools

Use GitBucket MCP tools instead of GitHub MCP tools:

| Operation | GitBucket MCP Tool |
|-----------|-------------------|
| Get issue | `gitbucket_get_issue` |
| Create issue | `gitbucket_create_issue` |
| Update issue | `gitbucket_update_issue` |
| Add comment | `gitbucket_add_issue_comment` |
| List issues | `gitbucket_list_issues` |

### Invoke GitBucket Skill

```
/skill gitbucket-api
```

This loads:
- Authentication patterns (token-only)
- Issue operation patterns
- Label operation limitations
- Error recovery procedures

### When to Use

- Remote URL contains non-GitHub domain
- Session init output: `GIT_PLATFORM=gitbucket`
- API calls fail with "Not Found" or "Bad credentials"

---

*Source: `020-github-workflow.md` (will be deprecated)*