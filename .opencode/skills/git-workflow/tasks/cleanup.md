# Task: cleanup

## Purpose

Delete merged branches after PR merge, clean stale references, and verify repository state is ready for next work session.

## Operating Protocol

1. **After PR merge:** Run when human confirms "PR merged" or similar
2. **Automatic detection:** Can also run when invoked to check for merged branches
3. **Mandatory cleanup:** ALL merged branches must be deleted (local and remote)

## Entry Criteria

- Human confirms "PR merged" or similar
- OR skill invoked with cleanup detection enabled

## Exit Criteria

- Local merged branch deleted
- Remote merged branch deleted (if applicable)
- Stale remote references pruned
- Other merged branches cleaned up
- Working tree clean

## Chat Output Format (CRITICAL)

**⚠️ CRITICAL: Cleanup reports to CHAT ONLY. Do NOT post to GitHub Issue.**

Cleanup is a local workflow (branch deletion, reference cleanup). It belongs in chat for developer visibility, not in the GitHub Issue permanent record.

### Chat Output Sequence

**Step 1: Start notification**
```
Cleanup starting after PR merge confirmation...
```

**Step 2: Progress updates (chat only)**
```
✓ Switched to main
✓ Deleted local branch: <branch-name>
✓ Deleted remote branch: <branch-name>
✓ Pruned stale references
```

**Step 3: Final completion (chat only)**
```
Cleanup complete. Ready for next task.

Issue #<number>: https://github.com/<owner>/<repo>/issues/<number>
```

### 🚫 FORBIDDEN Chat Outputs

| Forbidden Output | Reason |
|------------------|--------|
| "Performing cleanup after PR #X merged" | Too verbose before merge confirmed |
| Detailed step logs in GitHub Issue | Cleanup is local-only, not issue content |
| "Ready for next task?" prompts | HALT after completion, no prompting |
| Asking "Should I close issues?" | Close issues automatically, no asking |

### 🚫 NO GITHUB ISSUE POSTING

**Cleanup does NOT post comments to GitHub Issues except for:**
- Issue closure via `github_issue_write(method="update", state="closed")`
- Sub-issue verification (checking if platform auto-closed)

**Why no issue comments:**
- Cleanup is local git state management
- Branch deletions don't belong in issue permanent record
- Developer needs real-time visibility (chat) during cleanup
- Issues track implementation work, not git cleanup

### Correct Chat Output Sequence

```
User: "pr merged"

Agent (chat):

Cleanup starting after PR merge confirmation...
✓ Switched to main
✓ Deleted local branch: spec/git-workflow-skills
✓ Remote branch already deleted by GitHub
✓ Pruned stale references

Cleanup complete. Ready for next task.

Issue #143: https://github.com/NewsRx/gitbucket-mcp/issues/143

[HALT]
```

## Procedure

### Step 0: Get PR Context (First)

**Before any cleanup steps, get PR and issue context.**

```python
# From session context or parameter:
pr_number = <PR number that was merged>
branch_name = <branch that was merged>

# Get issue number from PR body or parameter:
issue_number = <issue being closed>
```

### Step 1: Report Start (Chat Only)

Report to chat:

```
Cleanup starting after PR merge confirmation...
```

**Do NOT post to GitHub Issue.**

### Step 2: Verify PR Merge (CRITICAL - NO EXCEPTIONS)

### Step 2: Verify PR Merge (CRITICAL - NO EXCEPTIONS)

**🚫 CRITICAL VIOLATION: Closing issues without PR merge verification is a CRITICAL GUIDELINE VIOLATION.**

**DO NOT trust `git pull` or local fast-forward. You MUST verify via GitHub API.**

```python
# MUST use GitHub API to verify merge
pr = github_pull_request_read(method="get", owner=..., repo=..., pullNumber=...)

# Verify merged_at timestamp exists
if pr.get("merged_at") is None:
    # PR is not merged, STOP
    report = f"PR #{pullNumber} is not yet merged. Cannot close issues."
    return report

# ONLY after verified merge:
proceed_to_close_issues()
```

**Why API verification is mandatory:**

### Step 3: Switch to Main and Report (Chat Only)

```bash
git checkout main
git pull origin main
```

Report to chat:

```
✓ Switched to main
```

### Step 4: Delete Branch and Report (Chat Only)

```bash
# Delete local branch
git branch -d <merged-branch-name>

# Delete remote branch (if not auto-deleted by GitHub)
git push origin --delete <merged-branch-name> 2>/dev/null || echo "Remote already deleted"

# Prune stale remote references
git fetch --prune
```

Report to chat:

```
✓ Deleted local branch: <branch-name>
✓ Deleted remote branch: <branch-name>  # or "Remote already deleted by GitHub"
✓ Pruned stale references
```

### Step 5: Final Report (Chat Only)

**After all cleanup steps, report final status to chat:**

```
Cleanup complete. Ready for next task.

Issue #<number>: https://github.com/<owner>/<repo>/issues/<number>
```

**Then HALT. No prompts, no questions, no "What's next?".**

### Step 6: Clean Other Merged Branches (Optional)

**Find merged branches:**
```bash
git branch --merged main
```

**For each merged branch (except main/master):**
```bash
git branch -d <branch>
```

### Step 7: Verify Clean State

```bash
git status --porcelain  # Must be empty
git branch -vv          # Should show minimal branches
```

## Context Required

- Guidelines: `114-git-branch-cleanup.md`, `124-github-archive-workflow.md`
- Related skills: `approval-gate` (issue closure timing)
- Related tasks: `pr-creation` (after this), `review-prep` (before PR)

## Branch Status Decision Tree

```
Merged PR (current branch just merged)
    │
    ├─► Switch to main: git checkout main
    │
    ├─► Pull latest: git pull origin main
    │
    ├─► Delete local: git branch -d <branch>
    │
    ├─► Delete remote: git push origin --delete <branch>
    │
    └─► Prune: git fetch --prune

Merged PR (other branches from previous sessions)
    │
    ├─► List merged: git branch --merged main
    │
    └─► For each (except main/master):
            git branch -d <branch>
```

## Safety Checks Before Deletion

Before ANY branch deletion:

1. **Merged status:** `git branch --merged main` includes the branch ✓
2. **GitHub PR status:** PR is "merged" (not "closed") ✓
3. **Not current branch:** `git branch --show-current` ≠ branch to delete ✓
4. **Not protected:** Branch name ≠ `main`, `master` ✓
5. **Clean working tree:** `git status --porcelain` returns empty ✓

**If ANY check fails → SKIP that branch with warning.**

## Sub-Issue Closure Enforcement (CRITICAL)

**⚠️ CRITICAL: Sub-issues are closed by the platform via "Fixes #N" annotations, NOT manually by the agent.**

### 🚫 FORBIDDEN

- **Closing sub-issues after implementation but BEFORE PR merge**
- **Closing sub-issues when PR is created but not merged**
- **Manually closing sub-issues that have "Fixes #N" in PR description**
- **Closing sub-issues without verifying PR merge via GitHub API**

### ✅ REQUIRED WORKFLOW

**The platform (GitBucket/GitHub) closes issues automatically via "Fixes #N" annotations.**

1. **Implement sub-issue** → Create PR with `Fixes #N` in description
2. **PR created** → Report URL, HALT
3. **Human merges PR** → Platform automatically closes sub-issue
4. **User confirms "pr merged"** → Agent verifies merge via GitHub API
5. **Agent verifies sub-issues are closed** → API check (`state: "closed"`)
6. **If sub-issue still open (edge case)** → Agent closes it manually
7. **All sub-issues closed?** → Close parent issue

### Verification Sequence

```python
# Step 1: Verify PR merge via GitHub API
pr = github_pull_request_read(method="get", owner=..., repo=..., pullNumber=...)
if pr.get("merged_at") is None:
    halt("PR not merged yet")

# Step 2: Check all sub-issues are closed (platform should have done this)
children = github_issue_read(method="get_sub_issues", issue_number=parent)
open_children = [c for c in children if c["state"] == "open"]

if open_children:
    # Edge case: Platform failed to auto-close
    for child in open_children:
        github_issue_write(method="update", issue_number=child["number"], 
                          state="closed", state_reason="completed")

# Step 3: Close parent only after all children closed
if not open_children:
    github_issue_write(method="update", issue_number=parent,
                       state="closed", state_reason="completed")
```

### "Fixes #N" Annotation (MANDATORY)

**PR descriptions MUST include sub-issue numbers:**

```markdown
Fixes #86, #87, #88

[PR body...]
```

This enables automatic closure by GitBucket/GitHub.

### Edge Case Handling

| Scenario | Action |
|----------|--------|
| Platform fails to auto-close sub-issue | Agent closes manually after PR merge verification |
| PR closed without merge | Sub-issues remain open (correct behavior) |
| Draft PR | Sub-issues remain open until PR is merged (correct behavior) |
| Multiple sub-issues in one PR | Include all in "Fixes #N, #M, #P" annotation |

## Sub-Issue Double-Check (CRITICAL)

After closing child issues addressed by PR, ALWAYS verify remaining sub-issues before closing parent.

**This requires agent intelligence, not just script logic.**

### Step 1: Query Sub-Issues

```python
children = github_issue_read(method="get_sub_issues", issue_number=parent_issue)
```

### Step 2: Classify Each Sub-Issue

**Already Closed:**
- `state: "closed"` + `state_reason: "completed"` → Done
- `state: "closed"` + `state_reason: "not_planned"` → Intentionally not done
- Closed with "Superseded by #N" comment → Check replacement exists

**Open but May Be Complete:**
- Check comments for "Superseded by #N" → Verify new issue covers work
- Check body for PR link ("Fixes #N") → If merged, work is done

**Open and Incomplete:**
- No PR, no superseded link, no completion comment → BLOCK parent closure

### Step 3: Take Action

```python
open_children = [c for c in children if c.state == "open"]

if open_children:
    # Classify each open child
    truly_incomplete = []
    
    for child in open_children:
        # Agent intelligence required here:
        # - Check state_reason
        # - Check comments for superseded links
        # - Check for merged PR links
        # - Determine if work is actually done
        
        if child_is_truly_incomplete(child):
            truly_incomplete.append(child)
    
    if truly_incomplete:
        # POST WARNING - do NOT close parent
        post_warning_comment(parent, truly_incomplete)
        # DO NOT close parent
    else:
        # All open children have justification
        close_parent_with_summary(parent)
else:
    # All children closed
    close_parent_with_summary(parent)
```

### Step 4: Warning Comment Template

If parent cannot be closed:

```markdown
🤖 ⚠️ **Cannot Close Parent — Open Sub-Issues Detected**

This parent issue cannot be closed because the following sub-issue(s) remain incomplete:

- #N: [Title] — [status analysis]

**Status Analysis:**
- [Explain why each open child cannot be closed]

**To close this parent:**
1. Complete the remaining sub-issue(s)
2. Close each sub-issue when work is complete
3. Or close as "not planned" with explanation if intentionally skipped

---
🤖 ⚠️ Blocked by OpenCode (ollama-cloud/glm-5)
```

**See Also:** `.opencode/guidelines/124-github-archive-workflow.md` → "Parent Closure Pre-Check" section for detailed logic.

## Common Issues

| Issue | Resolution |
|-------|------------|
| Remote branch already deleted | Skip remote deletion, clean local |
| Local has extra commits | Warn user, ask before deleting |
| Multiple PRs from same branch | Wait until ALL PRs merged |
| Stash exists from pre-work | Preserve stash, inform user |

## Automatic Cleanup Detection

When invoked, can check for merged branches:

```python
# Query GitHub for merged PRs
github_list_pull_requests(state="merged", perPage=50)

# For each merged PR:
#   - Check if local branch exists
#   - Check if merged into main
#   - Report cleanup candidate
```

## Why This Task Is Critical

- Feature branches accumulate over time
- Previous sessions may leave merged branches uncleaned
- Stale remote references clutter `git branch -a`
- Clean repository state required for next work session
- Prevents confusion from stale branch references
- **Issues ONLY closed after VERIFIED PR merge**

## Correct vs Incorrect Workflow

### ✅ CORRECT Workflow (Issue Closure)

```
PR created
    ↓
Developer reviews and merges PR
    ↓
Developer confirms "PR merged"
    ↓
cleanup task invoked
    ↓
Verify merge via GitHub API (merged_at field)
    ↓
API confirms merge → Proceed
    ↓
Close child issues addressed by PR
    ↓
Check parent for remaining sub-issues
    ↓
If all children closed → Close parent with summary
```

### 🚫 INCORRECT Workflow (CRITICAL VIOLATION)

```
PR created (or just branch pushed)
    ↓
Immediately close issues (NO MERGE)
    ↓
NO GitHub API verification
NO PR merge status check
NO parent/child structure check
```

**This incorrect workflow VIOLATES critical rules and causes:**
- Issues closed without PR tracking
- No merge verification
- Potential reopen of closed issues if PR rejected
- Lost audit trail

## Final HALT (CRITICAL)

**After closing issues and posting final summary, the agent MUST HALT.**

**HALT = Stop all further action. No prompting, no questions, no next steps.**

### What HALT Means After Cleanup

| Action | Status |
|--------|--------|
| Close issues | ✅ Done |
| Delete branches | ✅ Done |
| Post final summary | ✅ Done |
| Ask "What's next?" | 🚫 NEVER |
| Prompt for next task | 🚫 NEVER |
| Suggest new work | 🚫 NEVER |

**The workflow is complete. The agent stops. The human decides what happens next.**

### Correct Final Output

**Chat output (all cleanup progress reports):**

```
Cleanup starting after PR merge confirmation...
✓ Switched to main
✓ Deleted local branch: spec/github-issue-creation-skill
✓ Remote branch already deleted by GitHub
✓ Pruned stale references

Cleanup complete. Ready for next task.

Issue #81: https://github.com/NewsRx/gitbucket-mcp/issues/81
```

**GitHub Issue activity:**
- Issue closed via `github_issue_write(method="update", state="closed")`
- NO comments posted for cleanup progress
- Only closure action

**That's it. Chat has all progress. Issue closed. Then stop.**

### 🚫 CRITICAL VIOLATIONS After Cleanup

| Violation | Example |
|-----------|---------|
| Continue without new instruction | "Ready for next task?" |
| Suggest next work | "Should I start on #75?" |
| Prompt for anything | "What would you like me to do?" |
| Not posting final summary | Missing executive summary |

**The cleanup task is the END. HALT means STOP.**