# Task: pr-creation

## Purpose

Create pull request after explicit user instruction. Squash commits to single commit, push branch, create PR via GitHub MCP.

## Operating Protocol

1. **User-initiated only:** This task runs when user says "create a PR" or similar
2. **Squash to single commit:** ALL implementation commits combined into ONE clean commit
3. **HALT after PR creation:** Wait for human to merge

## Entry Criteria

- User says "create a PR", "make a PR", "push and create PR", or similar
- Implementation is complete
- Developer has reviewed changes via compare URL

## Procedure

### Step 0: Verify PR Instruction (MANDATORY FIRST)

**🚫 CRITICAL: This is an ENFORCEMENT GATE, not just documentation.**

**If ANY check fails → STOP and report. DO NOT proceed.**

#### Enforcement Gate (MUST PASS ALL)

**Before creating ANY PR, verify ALL conditions:**

```
□ Condition 1: Explicit PR instruction detected
  - "create a PR", "make a PR", "push and create PR", "let's get a PR up"
  - Implementation complete alone does NOT satisfy this check
  
□ Condition 2: review-prep was completed
  - Compare URL was generated and reported in chat
  - Developer had opportunity to review via GitHub diff
  
□ Condition 3: Branch was pushed to remote
  - git branch -vv shows [origin/branch]
  - Compare URL will work correctly
  
If ANY condition NOT satisfied → STOP and report.
```

#### PR Instruction Verification

1. **Check for PR instruction:**
   
   **Valid PR instructions (PROCEED):**
   - "create a PR"
   - "make a PR"
   - "push and create PR"
   - "let's get a PR up"
   - "open a PR"
   - "create pull request"
   - "pr" (shorthand)
   
   **What does NOT authorize PR creation (HALT):**
   
   | Phrase | Reason |
   |--------|--------|
   | "approved" | Authorizes implementation ONLY, NOT PR creation |
   | "go" | Authorizes implementation ONLY, NOT PR creation |
   | Implementation complete | Does NOT authorize PR - wait for explicit instruction |
   | "continue" | Ambiguous - could mean next phase |
   | "proceed" | Ambiguous - could mean next task |
   | "fix the skill and guideline" | Implementation instruction, NOT PR instruction |

2. **Authorization scope table:**

   | Authorization | What It Authorizes |
   |--------------|---------------------|
   | `approved` / `go` | Implementation ONLY |
   | `approved: X.Y` | Phase X.Y ONLY |
   | Implementation complete | NOTHING - wait for "create a PR" |
   | `create a PR` | PR creation workflow |
   | `create pull request` | PR creation workflow |

3. **Enforcement matrix:**

   | Scenario | Action |
   |----------|--------|
   | User says "create a PR" | ✅ PROCEED with PR creation |
   | User says "approved" only | ⛔ HALT - "approved authorizes implementation, not PR. Wait for 'create a PR' instruction." |
   | Implementation complete, no PR instruction | ⛔ HALT - report completion, wait for PR instruction |
   | User asks "ready for PR?" | ⛔ HALT - question, not instruction |
   | User says "fix X" (implementation only) | ⛔ HALT - implementation instruction, not PR instruction |

#### Verification Checklist

**BEFORE creating PR, confirm:**

```
✅ Explicit "create a PR" instruction present
✅ review-prep completed (compare URL reported)
✅ Developer had chance to review
✅ Branch pushed to remote
✅ Ready to squash and create PR
```

**If ANY checkbox unchecked → STOP and report what's missing.**

#### HALT Messages

**Implementation authorization is NOT PR authorization:**
```
PR creation requires explicit instruction.

User said 'approved' which authorizes implementation ONLY, not PR creation.

After implementation completes:
1. Report completion (exec summary + compare URL)
2. HALT and wait for developer review
3. Wait for explicit 'create a PR' instruction

To create PR: Say 'create a PR' or 'make a PR' explicitly.
```

**No PR instruction after implementation:**
```
Implementation complete. Awaiting PR instruction.

Current state:
- Implementation done
- Branch pushed
- Compare URL generated

Before creating PR:
1. Developer reviews changes via compare URL
2. Developer says 'create a PR' explicitly

To create PR: Say 'create a PR' when ready.
```

**Question detected (not instruction):**
```
Question detected - not PR instruction.

User asked: "Ready for PR?"

This is a question, not an instruction to create PR.

Correct next step:
1. Report completion (if not already done)
2. Present compare URL (if not already done)
3. HALT and wait for explicit 'create a PR'

To create PR: Say 'create a PR' explicitly, not as a question.
```

### Step 1: Changelog Generation

**Invoke changelog-generator skill as sub-task for context isolation.**

The skill MUST run as a sub-task (`/skill changelog-generator`) to prevent its thinking, output, and intermediate results from polluting the main session context.

#### Check Skip Directive

Before invoking the skill, check for `[skip changelog]` in:
- Last commit message (if squashing multiple commits)
- PR title

If `[skip changelog]` present, skip to Step 2.

#### Invoke Skill as Sub-Task

```
/skill changelog-generator --since-last-release
```

**Sub-Task Context Isolation:**
- Skill runs in its own context (isolated thinking)
- Skill analyzes commits, categorizes changes, generates changelog
- Skill writes CHANGELOG.md to filesystem
- Only minimal confirmation returns to main context
- Main context sees: "CHANGELOG.md updated with N entries"

#### Stage Changelog After Sub-Task

After sub-task completes:

```bash
git add CHANGELOG.md
```

Then continue to Step 2 (squash) — changelog changes bundled with code changes.

### Step 2: Squash to Single Commit

**MANDATORY:** All PRs must have exactly ONE commit.

```bash
git reset --soft origin/main
git commit -m "<descriptive message>" \
    --trailer "Co-authored-by: <AI-Name> (<model-id>) <ai-email>" \
    --trailer "Co-authored-by: <Human-Name> <human-email>"
```

### Step 3: Push to Remote

```bash
git push --force-with-lease origin <branch>
```

### Step 4: Collect Sub-Issues (Multi-Task Specs)

**For specs with sub-issues:**

```python
# Fetch all sub-issues for the parent issue
sub_issues = github_issue_read(method="get_sub_issues", issue_number=<parent>)

# Build autoclose list: parent + all sub-issues
autoclose_issues = [<parent>] + [sub["number"] for sub in sub_issues]
```

**For single-task specs:**

No sub-issues needed. Include only parent issue.

**⚠️ CRITICAL: Sub-issues are closed by the platform, NOT by the agent.**

- The "Fixes #N" annotation in PR body triggers automatic closure
- Agent does NOT manually close sub-issues after implementation
- Agent does NOT close sub-issues after PR creation
- Agent verifies closure AFTER PR merge via GitHub API
- Only in edge case (platform fails) does agent manually close

### Step 5: Create PR via GitHub MCP

```python
github_create_pull_request(
    owner=<GIT_OWNER>,
    repo=<GIT_REPO>,
    title="[SPEC] <description>",
    body="""<description>

Fixes #<parent>
Fixes #<child1>
Fixes #<child2>
...
""",
    head=<branch-name>,
    base="main"
)
```

**PR Body Requirements:**
- Must include `Fixes #<issue-number>` for autoclose
- Include ALL sub-issues for multi-task specs
- Brief description of changes

### Step 6: Report PR URL and HALT

### ⚠️ CRITICAL: PR URL Reporting is MANDATORY

**You MUST report exec summary + PR URL in chat:**

```
**Summary:**

<1-2 sentences describing the impact and stakeholder value.>

**Outcome:** <What changed for stakeholders>

**PR URL:** https://github.com/<owner>/<repo>/pull/<number>

Wait for human to merge.
```

**Format Requirements:**
- Executive summary FIRST (provides context)
- PR URL LAST (clickable link)
- MUST include "Wait for human to merge"

### What If PR Creation Fails?

| Failure Reason | Response |
|----------------|----------|
| No commits between branches | Report: "Branch has no commits to main. Changes may already be merged. Verify and HALT." |
| Branch conflicts | Report: "Branch conflicts with main. Rebase and push, then create PR." |
| GitHub API error | Report error details and HALT |

### Post-PR Creation Checklist

- [ ] Exec summary posted in chat
- [ ] PR URL posted in chat
- [ ] HALT — waiting for human merge

**🚫 NEVER:** Skip reporting PR URL, merge PR, or proceed without developer confirmation.

## Context Required

- Guidelines: `113-git-pr-workflow.md`
- Related skills: `pr-creation-workflow` (PR timing)
- Related tasks: `review-prep` (push before), `cleanup` (after merge)

## Co-Author Trailers (MANDATORY)

Every squash commit MUST include:
1. AI Author trailer
2. Human Collaborator trailer

**AI Trailer Format:**
- Use dynamic model detection at runtime
- Format: `Co-authored-by: <AI-Name> (<model-id>) <noreply@example.com>`
- Example: `Co-authored-by: OpenCode (glm-5) <noreply@opencode.ai>`

**Human Trailer:**
- Use session values from `000-session-init.md`
- `DEV_NAME`: Human's name
- `DEV_EMAIL`: Human's email
- Format: `Co-authored-by: <Human-Name> <human-email>`

## Sub-Issue Autoclose

| Spec Type | PR Body Format |
|-----------|---------------|
| Single-task | `Fixes #<parent>` |
| Multi-task | `Fixes #<parent>` AND `Fixes #<child>` for each sub-issue |

**Example Multi-Task PR Body:**

```markdown
Implemented sub-task architecture for skills.

Fixes #469
Fixes #470
```

## Common Issues

| Issue | Resolution |
|-------|------------|
| Multiple commits in PR | Run `git reset --soft origin/main` and re-commit |
| PR body missing Fixes | Verify sub-issues, add all to body |
| Branch conflicts | Rebase on main: `git rebase origin/main` |

## After PR Creation

1. Report PR URL
2. HALT — wait for human merge
3. Do NOT merge (human-only operation)