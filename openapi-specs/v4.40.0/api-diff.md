# GitBucket API Baseline - Version 4.40.0

**Release Date:** 2023-10-22  
**Commit SHA:** c909bc4b19f02688adc479c6e42000539476112e  
**Release Notes:** https://github.com/gitbucket/gitbucket/releases/tag/4.40.0

---

## Overview

This document describes the baseline API endpoints for GitBucket 4.40.0. This is the **first version** being tracked, so there is no prior version comparison. All existing API endpoints are documented here as the baseline for future version comparisons.

---

## Authentication

GitBucket supports multiple authentication methods:

### 1. Personal Access Token (Bearer)

```
Authorization: token YOUR_TOKEN
```

### 2. Basic Authentication

```
Authorization: Basic base64(username:password)
```

### 3. OAuth Token (as query parameter)

```
GET /api/v3/user?access_token=YOUR_TOKEN
```

### 4. Session-based Authentication

Uses browser session cookie for authenticated web UI access.

---

## GitHub API Compatibility

GitBucket implements a **subset** of the GitHub API v3. Not all GitHub endpoints are supported. The documented endpoints represent the complete API surface for GitBucket 4.40.0.

### Key Differences from GitHub API

| Feature | GitHub | GitBucket 4.40.0 |
|---------|--------|------------------|
| Rate Limiting | Yes | No (returns error) |
| Gists | Yes | No |
| Apps/GitHub Apps | Yes | No |
| Projects (beta) | Yes | Limited |
| Actions | Yes | No |
| Packages | Yes | No |
| Codespaces | Yes | No |
| Security advisories | Yes | No |

### GitBucket-Specific Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v3/gitbucket/plugins` | List installed plugins (non-standard) |

---

## API Endpoint Categories

### Root Endpoint

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3` | API metadata endpoint |
| GET | `/api/v3/rate_limit` | Returns "not enabled" error |

---

### Users API (8 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/user` | Get authenticated user |
| PATCH | `/api/v3/user` | Update authenticated user |
| GET | `/api/v3/users` | List all users |
| GET | `/api/v3/users/{username}` | Get a single user |
| GET | `/api/v3/users/{username}/repos` | List user repositories |
| GET | `/api/v3/users/{username}/orgs` | List user organizations |
| PUT | `/api/v3/users/{username}/suspended` | Suspend user (admin) |
| DELETE | `/api/v3/users/{username}/suspended` | Unsuspend user (admin) |

---

### Repositories API (6 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repositories` | List all repositories |
| GET | `/api/v3/repos/{owner}/{repo}` | Get repository |
| GET | `/api/v3/user/repos` | List authenticated user's repos |
| POST | `/api/v3/user/repos` | Create user repository |
| GET | `/api/v3/users/{username}/repos` | List user's repositories |
| POST | `/api/v3/orgs/{org}/repos` | Create org repository |
| GET | `/api/v3/orgs/{orgName}/repos` | List org repositories |

---

### Branches API (6 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/branches` | List branches |
| GET | `/api/v3/repos/{owner}/{repo}/branches/{branch}` | Get branch |
| PATCH | `/api/v3/repos/{owner}/{repo}/branches/{branch}` | Update branch protection |
| GET | `/api/v3/repos/{owner}/{repo}/branches/{branch}/protection` | Get branch protection |
| DELETE | `/api/v3/repos/{owner}/{repo}/branches/{branch}/protection` | Remove branch protection |
| GET | `/api/v3/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks` | Get required status checks |
| GET | `/api/v3/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts` | Get required status check contexts |

**Note:** GitBucket uses wildcard paths (`*`) for branch endpoints, allowing for branch names with slashes.

---

### Collaborators API (4 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/collaborators` | List collaborators |
| GET | `/api/v3/repos/{owner}/{repo}/collaborators/{username}` | Check collaborator |
| PUT | `/api/v3/repos/{owner}/{repo}/collaborators/{username}` | Add collaborator |
| DELETE | `/api/v3/repos/{owner}/{repo}/collaborators/{username}` | Remove collaborator |
| GET | `/api/v3/repos/{owner}/{repo}/collaborators/{username}/permission` | Get collaborator permission |

---

### Commits API (3 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/commits` | List commits |
| GET | `/api/v3/repos/{owner}/{repo}/commits/{sha}` | Get commit |
| GET | `/api/v3/repos/{owner}/{repo}/commits/{sha}/branches-where-head` | Get branches where head |

---

### Contents API (3 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/contents` | Get repository contents |
| GET | `/api/v3/repos/{owner}/{repo}/contents/{path}` | Get file/directory contents |
| PUT | `/api/v3/repos/{owner}/{repo}/contents/{path}` | Create or update file contents |
| GET | `/api/v3/repos/{owner}/{repo}/readme` | Get README |

**Note:** GitBucket uses wildcard paths (`*`) for contents endpoints to handle nested paths.

---

### Git References API (5 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/git/ref/{ref}` | Get a reference |
| GET | `/api/v3/repos/{owner}/{repo}/git/refs` | List references |
| POST | `/api/v3/repos/{owner}/{repo}/git/refs` | Create a reference |
| GET | `/api/v3/repos/{owner}/{repo}/git/refs/{ref}` | Get a reference (alternate) |
| PATCH | `/api/v3/repos/{owner}/{repo}/git/refs/{ref}` | Update a reference |
| DELETE | `/api/v3/repos/{owner}/{repo}/git/refs/{ref}` | Delete a reference |

---

### Issues API (5 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/issues` | List issues |
| POST | `/api/v3/repos/{owner}/{repo}/issues` | Create issue |
| GET | `/api/v3/repos/{owner}/{repo}/issues/{number}` | Get issue |
| GET | `/api/v3/repos/{owner}/{repo}/issues/{number}/comments` | List issue comments |
| POST | `/api/v3/repos/{owner}/{repo}/issues/{number}/comments` | Create issue comment |

---

### Issue Comments API (3 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/issues/comments/{id}` | Get comment |
| PATCH | `/api/v3/repos/{owner}/{repo}/issues/comments/{id}` | Update comment |
| DELETE | `/api/v3/repos/{owner}/{repo}/issues/comments/{id}` | Delete comment |

---

### Issue Labels API (9 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/labels` | List labels |
| POST | `/api/v3/repos/{owner}/{repo}/labels` | Create label |
| GET | `/api/v3/repos/{owner}/{repo}/labels/{name}` | Get label |
| PATCH | `/api/v3/repos/{owner}/{repo}/labels/{name}` | Update label |
| DELETE | `/api/v3/repos/{owner}/{repo}/labels/{name}` | Delete label |
| GET | `/api/v3/repos/{owner}/{repo}/issues/{number}/labels` | List labels for issue |
| POST | `/api/v3/repos/{owner}/{repo}/issues/{number}/labels` | Add labels to issue |
| PUT | `/api/v3/repos/{owner}/{repo}/issues/{number}/labels` | Replace issue labels |
| DELETE | `/api/v3/repos/{owner}/{repo}/issues/{number}/labels` | Clear issue labels |
| DELETE | `/api/v3/repos/{owner}/{repo}/issues/{number}/labels/{name}` | Remove label from issue |

---

### Milestones API (4 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/milestones` | List milestones |
| POST | `/api/v3/repos/{owner}/{repo}/milestones` | Create milestone |
| GET | `/api/v3/repos/{owner}/{repo}/milestones/{number}` | Get milestone |
| PATCH | `/api/v3/repos/{owner}/{repo}/milestones/{number}` | Update milestone |
| DELETE | `/api/v3/repos/{owner}/{repo}/milestones/{number}` | Delete milestone |

---

### Pull Requests API (8 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/pulls` | List pull requests |
| POST | `/api/v3/repos/{owner}/{repo}/pulls` | Create pull request |
| GET | `/api/v3/repos/{owner}/{repo}/pulls/{number}` | Get pull request |
| PATCH | `/api/v3/repos/{owner}/{repo}/pulls/{number}` | Update pull request |
| GET | `/api/v3/repos/{owner}/{repo}/pulls/{number}/commits` | List PR commits |
| GET | `/api/v3/repos/{owner}/{repo}/pulls/{number}/merge` | Check if merged |
| PUT | `/api/v3/repos/{owner}/{repo}/pulls/{number}/merge` | Merge pull request |

---

### Releases API (6 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/releases` | List releases |
| POST | `/api/v3/repos/{owner}/{repo}/releases` | Create release |
| GET | `/api/v3/repos/{owner}/{repo}/releases/latest` | Get latest release |
| GET | `/api/v3/repos/{owner}/{repo}/releases/tags/{tag}` | Get release by tag |
| PATCH | `/api/v3/repos/{owner}/{repo}/releases/{id}` | Update release |
| DELETE | `/api/v3/repos/{owner}/{repo}/releases/{id}` | Delete release |
| POST | `/api/v3/repos/{owner}/{repo}/releases/{id}/assets` | Upload release asset |
| GET | `/api/v3/repos/{owner}/{repo}/releases/{id}/assets/{asset_id}` | Get release asset |

---

### Commit Statuses API (4 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v3/repos/{owner}/{repo}/statuses/{sha}` | Create status |
| GET | `/api/v3/repos/{owner}/{repo}/commits/{ref}/status` | Get combined status |
| GET | `/api/v3/repos/{owner}/{repo}/commits/{ref}/statuses` | List commit statuses |
| GET | `/api/v3/repos/{owner}/{repo}/statuses/{ref}` | List statuses for ref |

---

### Webhooks API (4 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/hooks` | List webhooks |
| POST | `/api/v3/repos/{owner}/{repo}/hooks` | Create webhook |
| GET | `/api/v3/repos/{owner}/{repo}/hooks/{id}` | Get webhook |
| PATCH | `/api/v3/repos/{owner}/{repo}/hooks/{id}` | Update webhook |
| DELETE | `/api/v3/repos/{owner}/{repo}/hooks/{id}` | Delete webhook |

---

### Organizations API (2 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/orgs/{org}` | Get organization |
| GET | `/api/v3/organizations` | List organizations |
| GET | `/api/v3/user/orgs` | List user organizations |

---

### Raw Content API (1 endpoint)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/raw/{path}` | Get raw file content |

---

### Tags API (1 endpoint)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/repos/{owner}/{repo}/tags` | List repository tags |

---

### Admin API (2 endpoints)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v3/admin/users` | Create user (admin only) |
| POST | `/api/v3/admin/organizations` | Create organization (admin only) |

---

### Plugins API (1 endpoint)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v3/gitbucket/plugins` | List installed plugins |

**Note:** This is a GitBucket-specific endpoint, not part of the GitHub API.

---

## Total Endpoints

**93 API endpoints** documented in GitBucket 4.40.0 baseline.

---

## Release Notes (4.40.0)

### New Features

1. **Configurable default branch name**
2. **Custom fields support** for issues and pull requests in search conditions
3. **Pull request creation from fork default branch**
4. **News feed shows activities of all visible repositories**
5. **Drop Java 8 support** (Java 11+ required)
6. **Improve git push performance**

### Breaking Changes

- Java 8 runtime no longer supported

### API Impact

No documented breaking changes to the API in 4.40.0. All 93 endpoints should be compatible with GitHub API v3 clients.

---

## Known Limitations

### GitBucket vs GitHub API Differences

1. **Rate Limiting:** GitBucket does not implement rate limiting (returns error)
2. **No Gists API:** GitBucket does not support gists
3. **No GitHub Apps:** App installation endpoints not available
4. **Limited Projects:** Project boards have reduced functionality
5. **No Actions:** Workflows and CI/CD endpoints not available
6. **No Packages:** Package registry endpoints not available

### Authentication Notes

- Basic auth is supported but not recommended for production
- Token-based auth is the primary method
- Session auth is for web UI only
- Admin endpoints require administrative privileges

---

## Response Formats

All API responses use JSON format with content type `application/json`.

### Common Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Unprocessable Entity |

### Error Response Format

```json
{
  "message": "Error description",
  "documentation_url": "https://docs.github.com/rest"
}
```

---

## Pagination

GitBucket supports standard GitHub pagination:

### Request Parameters

- `page`: Page number (default: 1)
- `per_page`: Results per page (default: 30, max: 100)

### Response Headers

- `Link`: Pagination links for next/previous pages
- `X-Total-Count`: Total number of results

---

## Source Files

API controllers are located in:
```
src/main/scala/gitbucket/core/controller/api/
├── ApiUserControllerBase.scala
├── ApiRepositoryControllerBase.scala
├── ApiIssueControllerBase.scala
├── ApiIssueCommentControllerBase.scala
├── ApiIssueLabelControllerBase.scala
├── ApiIssueMilestoneControllerBase.scala
├── ApiPullRequestControllerBase.scala
├── ApiRepositoryBranchControllerBase.scala
├── ApiRepositoryCollaboratorControllerBase.scala
├── ApiRepositoryCommitControllerBase.scala
├── ApiRepositoryContentsControllerBase.scala
├── ApiRepositoryStatusControllerBase.scala
├── ApiRepositoryWebhookControllerBase.scala
├── ApiGitReferenceControllerBase.scala
├── ApiReleaseControllerBase.scala
└── ApiOrganizationControllerBase.scala
```

API models are located in:
```
src/main/scala/gitbucket/core/api/
├── ApiUser.scala
├── ApiRepository.scala
├── ApiIssue.scala
├── ApiComment.scala
├── ApiLabel.scala
├── ApiMilestone.scala
├── ApiPullRequest.scala
├── ApiBranch.scala
├── ApiCommit.scala
├── ApiRef.scala
├── ApiRelease.scala
├── ApiWebhook.scala
└── ... (and more model files)
```

---

## Reference Documentation

- **GitHub API v3:** https://docs.github.com/en/rest
- **GitBucket Documentation:** https://github.com/gitbucket/gitbucket/tree/master/doc
- **GitBucket Release Notes:** https://github.com/gitbucket/gitbucket/releases/tag/4.40.0

---

*Baseline established for GitBucket API v4.40.0. Future versions will document API differences as addenda to this specification.*