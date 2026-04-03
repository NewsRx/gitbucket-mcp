# Task: creation

## Purpose

Create GitHub Issue with proper title format, labels, and byline after validation passes.

## Operating Protocol

1. **Run after `pre-creation` validation passes.**
2. **DO NOT skip validation.**

## Entry Criteria

- Pre-creation validation passed
- Single-task vs multi-task determination complete
- User has authorized creation

## Exit Criteria

- Issue created in GitHub
- `needs-approval` label applied
- Creation byline appended to issue body (NOT a separate comment)
- Issue number available for sub-issue linking

## Procedure

### Step 1: Determine Title Format

| Issue Type | Title Format | Example |
|------------|--------------|---------|
| Primary spec | `[SPEC] <Feature Name>` | `[SPEC] PubMed API Rate Limiting` |
| Bug fix | `[SPEC-FIX] <Bug Description>` | `[SPEC-FIX] Token Refresh Failure` |
| Enhancement | `[SPEC-ENHANCEMENT] <Enhancement>` | `[SPEC-ENHANCEMENT] Add Rate Limiting` |
| Task | `[Task: #<parent>] <Task Description>` | `[Task: #100] Create user tables` |

### Step 2: Append Byline to Body (CRITICAL)

**🚨 CRITICAL: Append byline to body BEFORE creating issue.**

The byline MUST be appended to the issue body BEFORE calling `github_issue_write`, NOT as a separate comment after creation.

**Wrong Approach (VIOLATION):**
```python
# ❌ WRONG: Create issue first, then add byline as comment
issue = github_issue_write(method="create", body=body, ...)
github_add_issue_comment(..., body="🤖 ✨ Created by ...")  # BYLINE AS COMMENT
```

**Correct Approach:**
```python
# ✅ CORRECT: Append byline to body, then create issue
body_with_byline = f"""{body}

---

> **Approval Tracking**: Approvals tracked via comments.

🤖 ✨ Created by <AgentName> (<ModelID>)
"""

issue = github_issue_write(
    method="create",
    owner=owner,
    repo=repo,
    title=title,  # Format: [SPEC] <Description>
    body=body_with_byline,  # Body WITH byline already appended
    labels=["needs-approval"]
)
```

**Byline Format:**
- **Plain text emoji** (not inside italic/bold)
- Agent dynamically detects its own name and model ID
- **NEVER copy example values** — detect at runtime
- **Approval tracking separator** MUST be included before byline

### Step 3: Report Issue Created

Report: "Created issue #<number>. Next step: Invoke auditors before approval."

**Response includes:**
- `number`: Issue number (database ID)
- `id`: Database ID for sub-issue linking
- `html_url`: Issue URL

**IMPORTANT: NO separate byline comment needed - byline is in body.**

### Step 4: Report Issue Created

Report: "Created issue #<number>. Next step: Invoke auditors before approval."

## Multi-Task Spec Handling

**If spec has multiple phases:**

1. After creating parent issue
2. Invoke `github-sub-issues` skill
3. Create phase-level sub-issues
4. Link each via `github_sub_issue_write(method="add")`

**Single-task exemption:**
- If spec has ONE task, skip sub-issue creation
- Apply `needs-approval` label
- Proceed to `post-creation` task

## Safety Checks

Before proceeding, verify ALL:

- Pre-creation validation passed
- Title follows proper format
- `needs-approval` label applied
- Creation byline appended to body BEFORE issue creation
- Approval tracking separator included

**If ANY check fails → HALT and report.**

## Context Required

- Guidelines: `120-github-issue-first.md`, `123-github-ai-identity.md`
- Related tasks: `pre-creation` (runs first), `post-creation` (runs next)
- Related skills: `github-comments` (byline format), `github-sub-issues` (sub-issue creation)