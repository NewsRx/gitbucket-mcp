---
title: "[SPEC] Upstream GitBucket Release {VERSION} - OpenAPI Spec Update"
labels: ["api-sync","upstream","needs-approval"]
assignees: ["{REPO_OWNER}"]
---

# Spec: Upstream GitBucket Release {VERSION} - OpenAPI Spec Update

STATUS: 1.1
CREATED: {DATE}

---

## Objective

Update the OpenAPI specification to reflect API changes in GitBucket release {VERSION}.

---

## Upstream Release Details

| Field | Value |
|-------|-------|
| **Version** | {VERSION} |
| **Commit SHA** | {COMMIT_SHA} |
| **Release Date** | {PUBLISHED_DATE} |
| **Release Notes** | [{VERSION} Release Notes]({RELEASE_NOTES_URL}) |
| **Compare View** | [Changes from {PREV_VERSION}]({COMPARE_URL}) |

---

## Source Repository for Probing

**Repository URL:** https://github.com/gitbucket/gitbucket
**Git Clone URL:** https://github.com/gitbucket/gitbucket.git
**Default Branch:** master
**Release Tag:** {VERSION}
**Build System:** Scala/sbt

---

## Code Analysis Tools and Techniques

**⚠️ CRITICAL: Use code analysis tooling to perform thorough API analysis. Do NOT rely solely on release notes or web research.**

### Required Analysis Techniques

| Technique | Purpose | Commands/Approach |
|-----------|---------|-------------------|
| **Route Extraction** | Extract all API endpoints from controllers | `grep -rn 'get\("/api/v3\|post\("/api/v3\|put\("/api/v3\|patch\("/api/v3\|delete\("/api/v3' src/main/scala/gitbucket/core/controller/api/*.scala` |
| **Version Diff** | Compare API files between versions | Clone both versions, use `diff -u <old-file> <new-file>` on each API controller |
| **Endpoint Count** | Count total endpoints in each version | Count route definitions to detect additions/removals |
| **Schema Diff** | Detect API model changes | Diff `src/main/scala/gitbucket/core/api/*.scala` files between versions |
| **Build Analysis** | Check dependency changes | Analyze `build.sbt` for library version changes |
| **Service Layer** | Check business logic changes | Examine `src/main/scala/gitbucket/core/service/*.scala` for API-impacting changes |

### Analysis Workflow

1. **Clone both versions**:
   ```bash
   git clone --depth 1 --branch {PREV_VERSION} https://github.com/gitbucket/gitbucket.git ./tmp/gitbucket-prev
   git clone --depth 1 --branch {VERSION} https://github.com/gitbucket/gitbucket.git ./tmp/gitbucket-current
   ```

2. **Extract and count routes**:
   ```bash
   # Previous version
   grep -rn -E 'get\("/api/v3|post\("/api/v3|put\("/api/v3|patch\("/api/v3|delete\("/api/v3' \
     ./tmp/gitbucket-prev/src/main/scala/gitbucket/core/controller/api/*.scala \
     ./tmp/gitbucket-prev/src/main/scala/gitbucket/core/controller/ApiController.scala | wc -l

   # Current version
   grep -rn -E 'get\("/api/v3|post\("/api/v3|put\("/api/v3|patch\("/api/v3|delete\("/api/v3' \
     ./tmp/gitbucket-current/src/main/scala/gitbucket/core/controller/api/*.scala \
     ./tmp/gitbucket-current/src/main/scala/gitbucket/core/controller/ApiController.scala | wc -l
   ```

3. **Diff API controllers**:
   ```bash
   for file in ./tmp/gitbucket-prev/src/main/scala/gitbucket/core/controller/api/*.scala; do
     filename=$(basename "$file")
     diff -u "$file" "./tmp/gitbucket-current/src/main/scala/gitbucket/core/controller/api/$filename"
   done
   ```

4. **Diff API models**:
   ```bash
   for file in ./tmp/gitbucket-prev/src/main/scala/gitbucket/core/api/*.scala; do
     filename=$(basename "$file")
     diff -u "$file" "./tmp/gitbucket-current/src/main/scala/gitbucket/core/api/$filename"
   done
   ```

5. **Check service layer** (for behavior changes):
   ```bash
   diff -r ./tmp/gitbucket-prev/src/main/scala/gitbucket/core/service/ \
           ./tmp/gitbucket-current/src/main/scala/gitbucket/core/service/
   ```

### Key Directories to Analyze

| Directory | Purpose | Priority |
|-----------|---------|----------|
| `src/main/scala/gitbucket/core/controller/api/` | API route definitions | **CRITICAL** |
| `src/main/scala/gitbucket/core/controller/ApiController.scala` | Root API endpoint | **CRITICAL** |
| `src/main/scala/gitbucket/core/api/` | API models/schemas | **CRITICAL** |
| `src/main/scala/gitbucket/core/service/` | Business logic | **HIGH** |
| `build.sbt` | Dependencies and versions | **MEDIUM** |
| `src/main/scala/gitbucket/core/controller/` | Web UI controllers | **LOW** (API only) |

### What to Look For

- **Route additions**: New `get|post|put|patch|delete("/api/v3/...")` patterns
- **Route removals**: Routes present in old version but missing in new
- **Route modifications**: Changed route paths or parameters
- **Model changes**: Case class changes in `ApiIssue.scala`, `ApiPullRequest.scala`, etc.
- **Service changes**: Methods called by API controllers
- **Dependency changes**: Library upgrades in `build.sbt` that may affect API behavior

---

## Affected Files

| File | Description |
|------|-------------|
| `openapi-specs/v{VERSION}/openapi.json` | OpenAPI specification for this version |
| `openapi-specs/v{VERSION}/release-notes.md` | Relevant notes from release (if any) |
| `openapi-specs/v{VERSION}/api-diff.md` | API differences from prior version |

---

## Reference Documentation

Include any reference documentation that accompanies this spec as sibling files in `openapi-specs/v{VERSION}/`:
- API documentation files
- Schema definitions
- Migration notes (if applicable)

---

## API Differences from Prior Version

**Required for all releases except the first in tracking.**

Create `openapi-specs/v{VERSION}/api-diff.md` documenting:

1. **New Endpoints** - Any new API endpoints added
2. **Modified Endpoints** - Endpoints with changed parameters, responses, or behavior
3. **Deprecated Endpoints** - Endpoints marked for removal
4. **Removed Endpoints** - Endpoints deleted in this version
5. **Schema Changes** - Changes to request/response schemas
6. **Authentication Changes** - Changes to auth requirements
7. **Breaking Changes** - Changes that break backward compatibility
8. **Internal Changes** - Formatting-only changes, refactorings with no API impact
9. **Performance Improvements** - Backend changes that improve API performance

Use the compare view to analyze changes:
- GitHub Compare: https://github.com/gitbucket/gitbucket/compare/{PREV_VERSION}...{VERSION}
- Focus on `src/main/scala/gitbucket/core/api/` and `src/main/scala/gitbucket/core/controller/` directories

---

## Phase 1: Source Analysis (Gated)

### Steps

1. ☐ Clone upstream repository: `git clone https://github.com/gitbucket/gitbucket.git`
2. ☐ Checkout release tag: `git checkout {VERSION}`
3. ☐ Identify API endpoints in source code using grep and diff
4. ☐ Document API changes from previous version
5. ☐ Note any BREAKING CHANGES or deprecated endpoints
6. ☐ Create `openapi-specs/v{VERSION}/api-diff.md` documenting differences
7. ☐ Verify findings against release notes (release notes may miss internal changes)

---

## Phase 2: OpenAPI Specification (Gated)

### Steps

1. ☐ Create `openapi-specs/v{VERSION}/openapi.json`
2. ☐ Document all API endpoints from source analysis
3. ☐ Include request/response schemas
4. ☐ Document authentication requirements
5. ☐ Include any release notes relevant to API changes

---

## Phase 3: Verification (Auto-progress)

### Steps

1. ☐ Validate OpenAPI specification schema
2. ☐ Verify all endpoints documented
3. ☐ Check for breaking changes vs previous version
4. ☐ Verify api-diff.md accurately reflects changes

---

## Phase 4: Human Approval (Gated)

### Steps

1. ☐ Human review of OpenAPI specification
2. ☐ Human review of API differences document
3. ☐ Approve or request revisions

---

## Phase 5: State Update (Gated)

### AI Agent Responsibility

After PR merge confirms successful implementation:

1. ☐ Wait for PR merge confirmation (see `124-github-archive-workflow.md` for closure workflow)
2. ☐ Update state file:
   ```bash
   echo "{VERSION}" > workflow-state/last_release.txt
   git add workflow-state/last_release.txt
   git commit -m "chore: update state to {VERSION} after release processing"
   git push
   ```
3. ☐ Verify state file reflects processed version: `cat workflow-state/last_release.txt`

**CRITICAL:**
- State file should ONLY be updated after successful PR merge
- State semantics: "last processed version" (not "last detected")
- This enables the workflow to show backlog via state lag

**See `.opencode/guidelines/124-github-archive-workflow.md` for complete issue closure workflow.**

---

> **Approval Tracking**: Approvals are tracked via GitHub Issue comments.

---

## Release Notes (if relevant)

{RELEASE_NOTES_BODY}