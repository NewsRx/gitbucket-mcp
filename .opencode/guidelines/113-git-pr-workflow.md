# Git Protocol: PR Workflow

**See `pr-creation-workflow` skill for PR timing requirements including:**
- Authorization boundary (what authorizes implementation vs PR)
- Developer must test before PR
- HALT after PR creation

---

## Review Phase (Mandatory)

After implementation completes and BEFORE PR creation authorization:

1. **Agent pushes feature branch** to remote:
   ```bash
   git push -u origin <branch-name>
   ```

2. **Agent reports compare URL in CHAT ONLY** (NEVER to GitHub Issues):
   - URLs go in chat dialog ONLY
   - GitHub Issues receive completion comment WITHOUT URL

3. **Developer reviews changes** via GitHub diff viewer
4. **Developer decides** whether to create PR or request changes
5. **If satisfied, developer says** "create a PR"
6. **Agent creates PR** (squash, push, create PR, HALT)

**Why This Matters:**
- URLs in chat keep conversations clean
- Issues remain focused on task tracking, not URLs
- Developer can review changes before PR exists
- Clear separation between "implementation done" and "PR requested"

---

## 🚫 CRITICAL: PR Creation Without Authorization

**Creating a PR without explicit "create a PR" instruction is a CRITICAL GUIDELINE VIOLATION.**

### Enforcement Requirements

**PRs require EXPLICIT instruction:**
- "create a PR"
- "make a PR"
- "push and create PR"
- "let's get a PR up"

**What does NOT authorize PR creation:**
- "approved" or "go" → Authorizes implementation ONLY
- Implementation complete → NOT PR authorization
- "continue" or "proceed" → Ambiguous, not PR instruction
- "fix the skill" → Implementation instruction, not PR instruction

### Mandatory Sequence

```
Implementation complete
    ↓
review-prep invoked AUTOMATICALLY (Phase 3)
    ↓
Push branch → Generate compare URL → HALT
    ↓
(Developer reviews via GitHub diff)
    ↓
Developer says "create a PR" ← EXPLICIT instruction required
    ↓
pr-creation: Squash → Create PR → HALT
```

### What HALT Means After review-prep

**HALT = Stop all action and wait for explicit instruction.**

| Action | ✅ DO | 🚫 NEVER |
|--------|-------|----------|
| Report completion | Post exec summary + compare URL in chat | Skip reporting |
| Post issue comment | Completion comment (NO URL) | Post URL to issue |
| Wait for review | Stop and wait | Proceed to PR creation |
| Wait for instruction | Silent halt | Ask "ready for PR?" |

---

## 🚫 CRITICAL: Automatic Skill Invocation

**When a skill is invoked, EXECUTE it, not just read it.**

### The Problem

Skills are executable workflows, not reference documentation. When a skill is invoked:

| Wrong Behavior | Correct Behavior |
|----------------|------------------|
| Load skill content | Load skill content |
| Read the content | READ AND EXECUTE each step |
| Halt without action | Follow procedural steps |
| Report completion without doing work | Complete workflow then report |

### Violation Example

```
User: "pr merged"
    ↓
Agent invokes /skill git-workflow
    ↓
Agent loads skill content
    ↓
Agent HALTS without executing cleanup task ← CRITICAL VIOLATION
    ↓
User: "actually perform the appropriate skill"
```

**Correct Behavior:**
```
User: "pr merged"
    ↓
Agent invokes /skill git-workflow
    ↓
Agent EXECUTES cleanup task:
    1. Verify PR merge via GitHub API
    2. Switch to main
    3. Delete merged branch
    4. Clean up stale refs
    5. Post succinct confirmation
    ↓
HALT
```

### Why This Matters

- Skills encapsulate procedural knowledge
- Loading ≠ Executing
- The workflow must be followed, not just understood
- Halt happens AFTER execution, not during

---

## PR Requirements

- Reference issue: `Fixes #123` in PR description
- Pass CI checks
- **Human review required** — Copilot review is supplemental, not sufficient for merge

---

## 🚫 ABSOLUTE PROHIBITION: AGENTS MUST NEVER MERGE PRs

- **PR merging is HUMAN-ONLY.** The agent MUST NOT call `github_merge_pull_request` at any time.
- **ALL PRs require human review before merge** — no exceptions, no self-merging.
- **"go" does NOT authorize merging.** "go" means "proceed to the next task or phase" — NOT "merge the PR".
- After PR creation, the agent MUST report the PR URL and HALT.
- If PR is open and user says "go", the agent must clarify that merging requires explicit "merge" instruction.

---

## Enforcement Mechanisms

### Multi-Layer Defense

| Layer | Mechanism | Scope | Bypassable? |
|-------|-----------|-------|-------------|
| **Local** | `.githooks/pre-commit` | Blocks commit to main | No |
| **Local** | `.githooks/post-commit` | Warns after commit to main | N/A (post) |
| **GitHub** | Branch protection rules | Requires PR | No |

**There is NO emergency bypass.** If you need to make an urgent fix:
1. Create a feature branch: `git checkout -b hotfix/urgent-fix`
2. Make your changes and commit
3. Push and create PR with `hotfix` label
4. Request expedited review

### Recovery from Accidental Main Commit

If you somehow committed to main locally (hooks not installed):

```bash
# Create recovery branch from the commit
git branch feature/recovery HEAD

# Reset main to match remote
git checkout main
git reset --hard origin/main

# Switch to recovery branch
git checkout feature/recovery

# Push and create PR
git push origin feature/recovery
```

---

*Source: Content migrated from `110-git-protocol.md`*