# API Differences: GitBucket 4.45.0 → 4.46.0

**Version:** 4.46.0  
**Release Date:** 2026-04-03  
**Upstream Release Notes:** https://github.com/gitbucket/gitbucket/releases/tag/4.46.0

---

## Executive Summary

**No API changes detected between 4.45.0 and 4.46.0.**

All 112 API routes remain identical. No new endpoints, no removed endpoints, no modified request/response schemas.

---

## Source Verification Method

API changes were determined by:

1. **Direct source code comparison** between versions
2. **Route extraction** from Scala controller files
3. **API model comparison** for schema changes
4. **CHANGELOG analysis** (secondary verification only)

**⚠️ CRITICAL:** Release notes mentioned only UI changes (no API impact):

- Add new option to show full username on UI
- Support render plugin in issues, pull requests, wiki and commit comments  
- Support link to other pages from Wiki page using Wiki link syntax

---

## New Endpoints

**None detected.**

---

## Modified Endpoints

**None detected.**

---

## Deprecated Endpoints

**None marked for deprecation.**

---

## Removed Endpoints

**None removed.**

---

## Schema Changes

**No changes to request or response schemas.**

---

## Authentication Changes

**No changes to authentication requirements.**

---

## Breaking Changes

**None.**

This is a **non-breaking release** for API consumers. All existing integrations should continue to work without modification.

---

## Internal Changes (No API Impact)

The following internal changes have **no impact on API consumers**:

- UI rendering improvements
- Wiki link syntax support
- Plugin render support in comments

These changes affect only the frontend/presentation layer and do not alter API behavior.

---

## Performance Improvements

**No API performance changes identified.**

---

## Code Comment Gotchas

The following TODO/FIXME comments exist in API controller code (pre-existing, not new):

| File | Line | Comment |
|------|------|---------|
| ApiIssueMilestoneControllerBase.scala | 18 | `// TODO "sort", "direction" params should be implemented.` |
| ApiRepositoryCollaboratorControllerBase.scala | 17 | `// TODO Should ApiUser take permission?` |
| ApiPullRequestControllerBase.scala | 33 | `// TODO: more api spec condition` |
| ApiPullRequestControllerBase.scala | 232 | `// TODO: crash when body is empty` |
| ApiPullRequestControllerBase.scala | 233 | `// TODO: Implement sha parameter` |
| ApiPullRequestControllerBase.scala | 265 | `// TODO: Implement commit_title` |
| ApiIssueLabelControllerBase.scala | 47, 78 | `// TODO ApiError should support errors field` |
| ApiIssueControllerBase.scala | 26 | `// TODO: more api spec condition` |

These are **long-standing issues**, not introduced in 4.46.0.

---

## Migration Notes

**No migration required for API consumers.**

---

## Source Code References

| Component | File | Anchor |
|-----------|------|--------|
| API Routes | `src/main/scala/gitbucket/core/controller/api/*.scala` | All controllers |
| API Models | `src/main/scala/gitbucket/core/api/*.scala` | All model files |
| Main Controller | `src/main/scala/gitbucket/core/controller/ApiController.scala` | Route definitions |

---

**Generated:** 2026-04-03  
**Source:** Direct code comparison between release tags `4.45.0` and `4.46.0`