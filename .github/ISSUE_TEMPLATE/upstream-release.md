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
**Default Branch:** Discover from repository (run `git remote show origin` after clone)
**Release Tag:** {VERSION}

---

## Code Analysis Approach

**⚠️ CRITICAL: Source code comparison is the ONLY authoritative source for API changes.**

- **Do NOT trust release notes** - They may miss internal API changes or describe changes inaccurately
- **Do NOT trust CHANGELOG** - GitBucket 4.42.1 CHANGELOG said "Fix LDAP issue" but source analysis found internal API signature changes in `getBranchesNoMergeInfo()`
- **Do NOT trust migration guides** - They focus on user-visible changes, not API-level changes
- **Do NOT trust documentation** - Documentation may be outdated, incomplete, or describe intended behavior rather than actual behavior
- **TRUST ONLY** - Direct source code comparison between versions

### Analysis Philosophy

The remote development team may reorganize the codebase, change directory structures, or even change implementation languages between releases. Therefore:

1. **Discover structure dynamically** - Do not assume fixed paths
2. **Search semantically** - Look for patterns that define API routes, models, and schemas
3. **Adapt to the codebase** - Use the actual project structure found in each version
4. **Verify with source only** - Compare actual code between versions; never rely on documentation describing changes

### Analysis Workflow

1. **Clone both versions:**
   ```bash
   git clone --depth 1 --branch {PREV_VERSION} https://github.com/gitbucket/gitbucket.git ./tmp/gitbucket-prev
   git clone --depth 1 --branch {VERSION} https://github.com/gitbucket/gitbucket.git ./tmp/gitbucket-current
   ```

2. **Discover project structure:**
   - Identify the implementation language and framework
   - Locate build system files (discover what exists - don't assume specific files)
   - Find API route definitions by searching for endpoint patterns appropriate to the discovered framework
   - Find API models/schemas by searching for data structure definitions appropriate to the language

3. **Semantic search for API routes:**
   - Search for HTTP method patterns combined with path definitions
   - Look for route definition syntax appropriate to the language and framework discovered
   - Common patterns vary by framework: `@GetMapping`, `@app.route`, `get("path", ...)`, `#[get("path")]`, etc.
   - Discover the API path structure (versioned like `/api/v1`, unversioned like `/api`, or REST without prefix)
   - Adapt search patterns to the actual language/framework/API structure found

4. **Count and compare endpoints:**
   - Extract all API endpoints from both versions
   - Count total endpoints in each version
   - Identify added, removed, or modified routes

5. **Diff API-related files:**
   - Compare files that define API routes between versions
   - Compare files that define API models/schemas between versions
   - Focus on semantic changes (parameter types, return types, endpoint paths)

6. **Check behavior-impacting changes:**
   - Service layer changes (business logic)
   - Dependency changes in build files
   - Authentication/authorization changes

### What to Look For

| Category | Search Approach |
|----------|-----------------|
| **Route additions** | New endpoint definitions not in previous version |
| **Route removals** | Endpoints in previous version but missing in current |
| **Route modifications** | Changed paths, parameters, or HTTP methods |
| **Model changes** | Data structure changes affecting request/response schemas |
| **Service changes** | Methods called by API controllers |
| **Dependency changes** | Library upgrades affecting API behavior |

### Discovery Process

Before analyzing API changes, discover the project's actual structure, language, and framework. Do not assume specific directories, file names, or languages.

**What to discover:**

1. **Language and build system:** Identify what languages are used and how the project is built. Look for build configuration files, package managers, and source file extensions. Discover what exists, don't assume specific names.

2. **API versioning scheme:** Discover how the API is structured - is it versioned (`/api/v1`, `/api/v2`) or unversioned (`/api` or no prefix)? Search for HTTP method patterns in route definitions to understand the routing style.

3. **Route definition patterns:** Determine how API routes are defined in this project - annotations, function calls, router objects, decorators? Adapt search patterns to what you find.

4. **Controller/handler locations:** Find where route definitions live by searching for common naming patterns (`*controller*`, `*api*`, `*routes*`, `*handlers*`) rather than assuming fixed paths.

5. **Model/schema definitions:** Locate where request/response structures are defined. Look for data structure definitions appropriate to the discovered language.

**How to discover:** Use file system exploration, grep for patterns, examine build files, and analyze directory structure. Adapt your approach based on what you find.

**Critical:** The remote team may change languages, frameworks, directory structures, or naming conventions. Your discovery process must detect and adapt to whatever structure exists in each version.

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
8. **Internal Changes** - Changes with no API impact (refactorings, formatting)
9. **Performance Improvements** - Backend changes that improve API performance

**Format:** Keep api-diff.md minimal and focused on API changes visible to remote callers:
- Endpoint paths
- Request schemas
- Response schemas

**NOT:** Internal implementation changes (private methods, internal services)

**⚠️ Source Verification Required:** All findings must come from direct source code comparison between versions. Do not rely on release notes, CHANGELOG, or documentation to describe API changes - they may be incomplete or inaccurate.

---

## Phase 1: Source Analysis (Gated)

### Steps

1. ☐ Clone upstream repository: `git clone https://github.com/gitbucket/gitbucket.git`
2. ☐ Checkout release tag: `git checkout {VERSION}`
3. ☐ Discover project structure (language, build system, directory layout)
4. ☐ Identify API endpoints using semantic search adapted to discovered structure
5. ☐ Compare source code directly between versions (ONLY source code is authoritative)
6. ☐ Document API changes from direct source comparison
7. ☐ Note any BREAKING CHANGES or deprecated endpoints
8. ☐ Create `openapi-specs/v{VERSION}/api-diff.md` documenting differences
9. ☐ If release notes mention API changes, verify each claim against source code

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

After OpenAPI spec PR merge confirms successful implementation:

1. ☐ Wait for PR merge confirmation (see `124-github-archive-workflow.md` for closure workflow)
2. ☐ **Create feature branch FIRST** (see `110-git-branch-first.md`):
   ```bash
   git checkout main && git pull origin main
   git checkout -b chore/update-state-to-{VERSION}
   ```
3. ☐ Update state file:
   ```bash
   echo "{VERSION}" > workflow-state/last_release.txt
   ```
4. ☐ Commit with co-author trailers:
   ```bash
   git add workflow-state/last_release.txt
   git commit -m "chore: update state to {VERSION} after release processing" \
       --trailer "Co-authored-by: <AI-Name> (<model-id>) <noreply@ai-service>" \
       --trailer "Co-authored-by: <Human-Name> <human-email>"
   ```
5. ☐ Push and create PR:
   ```bash
   git push origin chore/update-state-to-{VERSION}
   gh pr create --title "chore: update state to {VERSION}" \
       --body "Updates last_release.txt after successful OpenAPI spec processing for {VERSION}"
   ```
6. ☐ Wait for human to merge PR
7. ☐ Verify state file after merge: `cat workflow-state/last_release.txt`

**CRITICAL:**
- State file updates require PR workflow (see `113-git-pr-workflow.md`)
- Branch-first is MANDATORY for ALL file modifications (see `110-git-branch-first.md`)
- Even "chore" commits require feature branches and PRs
- State semantics: "last processed version" (not "last detected")
- This enables the workflow to show backlog via state lag

---

> **Approval Tracking**: Approvals are tracked via GitHub Issue comments.

---

## Release Notes (if relevant)

{RELEASE_NOTES_BODY}