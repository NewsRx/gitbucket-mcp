# Task: pre-work

## Purpose

Verify branch state, preserve changes, create feature branch BEFORE any implementation work begins.

## Operating Protocol

1. **Automatic invocation (mandatory):** This task is invoked automatically when:
   - User says `approved`, `go`, or similar authorization to begin implementation
   - DO NOT prompt for invocation - the skill is triggered automatically

## Entry Criteria

- User has authorized implementation (explicit `approved` or `go`)
- Authorization is for the correct issue
- Sub-issue structure verified (for multi-task specs)

## Procedure

### Step 0: Verify Authorization (MANDATORY FIRST)

**🚫 CRITICAL: This check MUST happen BEFORE any git operations.**

#### Authorization Verification Protocol

1. **Extract issue context:**
   - Issue number from invocation context
   - Check authorization is explicit (not conditional)

2. **Query GitHub Issue:**
   ```python
   issue = github_issue_read(method="get", owner=OWNER, repo=REPO, issue_number=N)
   labels = [l["name"] for l in issue["labels"]]
   comments = github_issue_read(method="get_comments", owner=OWNER, repo=REPO, issue_number=N)
   ```

3. **Check for authorization:**
   
   **Explicit authorization (PROCEED):**
   - User said "approved" or "go" in comment
   - User said "#N approved" for THIS issue
   - User said "approved: X.Y" for THIS issue
   
   **Conditional phrases (HALT - NOT authorization):**
   - "continue if you have next steps"
   - "proceed when ready"
   - "if you have a plan, continue"
   - "after analysis, proceed"
   
   **Question phrases (HALT - seeking permission):**
   - "should I do X?"
   - "would you like me to X?"
   - "ready for you to continue"

4. **Enforcement matrix:**

   | Scenario | Action |
   |----------|--------|
   | `needs-approval` label + explicit "approved" | ✅ PROCEED - explicit auth wins |
   | `needs-approval` label + NO auth found | ⛔ HALT - "Authorization required. Issue has needs-approval label." |
   | NO label + explicit "approved" | ✅ PROCEED |
   | NO label + NO auth found | ⛔ HALT - "Authorization required. Say 'approved' or 'go'." |
   | Conditional phrase detected | ⛔ HALT - "Conditional phrase not authorization. Need explicit 'approved' or 'go'." |

5. **What does NOT authorize implementation:**
   
   | Phrase | Reason |
   |--------|--------|
   | "continue" | Ambiguous - could mean analysis |
   | "if you have next steps" | CONDITIONAL - not explicit |
   | "proceed with X" | Ambiguous without "approved"/"go" |
   | Analysis presented | NOT authorization |
   | Spec created | NOT authorization |
   | "should I do X?" | QUESTION - seeking permission |

6. **Authorization scope:**
   - Issue-bound: Applies ONLY to this issue
   - Phase-bound: "approved: 1.2" means phase 1.2 only
   - Session-bound: New session = new authorization needed

#### HALT Messages

**Missing authorization:**
```
Authorization required before proceeding.

Issue #N has needs-approval label and no explicit 'approved' or 'go' comment.

To authorize: Say 'approved' or 'go' in a comment.
```

**Conditional phrase detected:**
```
Conditional phrase detected - not explicit authorization.

User said: "Continue if you have next steps, or ask for clarification."

This requires agent to present next steps OR ask for clarification first.
Cannot proceed without explicit 'approved' or 'go'.

To authorize: Say 'approved' or 'go' explicitly.
```

**No authorization found:**
```
Authorization required before proceeding.

No 'approved' or 'go' comment found on issue #N.

To authorize: Say 'approved' or 'go' in a comment.
```

### Step 1: Check Current Git State

```bash
git branch --show-current
git status
```

If on `main` → stash changes then create feature branch.

### Step 2: Stash ALL Pending Changes (MANDATORY)

**ALWAYS stash before ANY branch operation. No exceptions.**

```bash
git stash push -u -m "WIP: before <branch-name>"
```

**The `-u` flag includes untracked files. This is mandatory.**

**What gets stashed:**
- Modified files
- Deleted files
- Untracked files
- Staged changes

### Step 3: Verify Stash Succeeded

```bash
git stash list  # VERIFY stash created
git status      # VERIFY clean working tree
```

**CRITICAL VERIFICATION:**

| Check | Command | Expected Result |
|-------|---------|------------------|
| Stash exists | `git stash list` | Shows stash entry |
| Working tree clean | `git status --porcelain` | Empty output |

**If EITHER check fails → STOP. Report failure. Let user resolve.**

### Step 4: Create Feature Branch

```bash
git checkout main && git pull origin main
git checkout -b spec/<short-name>  # or feature/<description>
```

### Step 5: Report Ready

Report: "Ready for implementation on branch: <branch-name>"

## ⚠️ Edge Case: Already Implemented (No Changes Needed)

**When investigation reveals spec is already implemented:**

1. **Detect before branch creation:**
   - After reading files, verify all proposed changes are already present
   - Confirm no modifications needed
   - Document verification in issue comment

2. **Skip branch creation entirely:**
   - Do NOT create feature branch
   - Do NOT push anything
   - Do NOT create PR

3. **Close issue directly:**
   - Post verification comment explaining what was checked
   - Close issue with `state_reason: "completed"`
   - Report completion in chat

**Example Comment:**
```markdown
🤖 ✅ Completed by <AgentName> (<ModelID>)

**Summary:**

Verified all proposed changes were already implemented. No modifications needed.

**Verification Results:**

- [List what was checked and confirmed present]
- [File references with function names for existing content]

**Outcome:** Spec requirements verified complete without additional changes.
```

4. **HALT after closing:**
   - No further steps needed
   - No branch cleanup (no branch was created)

## Context Required

- Guidelines: `110-git-branch-first.md`, `114-git-branch-cleanup.md`
- Related skills: `approval-gate` (authorization check)
- Related tasks: `cleanup` (branch cleanup after PR merge)

## Common Issues

| Issue | Resolution |
|-------|------------|
| Stash failed | STOP. Report failure. Let user resolve manually. |
| Wrong branch detected | STOP. Do not commit. Stash changes, switch to correct branch. |
| Accidental main commit | Create recovery branch, reset main, switch to recovery branch. |

## Safety Checks

Before proceeding, verify ALL:

- Current branch is NOT `main`
- Working tree IS clean (`git status --porcelain` returns empty)
- Branch name follows convention (`spec/` or `feature/` prefix)

**If ANY check fails → STOP and report.**

## Enforcement Checklist

**Before starting any work, verify:**

- ✅ Authorization received (explicit `approved`, `go`, or `"#N approved"`)
- ✅ Current branch is NOT `main` (or stash and create feature branch)
- ✅ Working tree is clean (`git status --porcelain` returns empty)
- ✅ Stash created if needed (`git stash list` shows entry)
- ✅ Feature branch created from `main`

**These checks are MANDATORY. If ANY check fails → STOP and report.**