# GitHub Workflow: AI Identity in Comments

**See `github-comments` skill for complete comment protocol.**

## 🤖 MANDATORY: Single Combined Byline Format

ALL comments on issues and PRs MUST have a SINGLE byline at the END combining status, agent, and model.

### Unified Byline Format

**Format:**
```
<response content>

---
🤖 <status-emoji> <status-text> by <AgentName> (<ModelID>)
```

**Components (supplied dynamically at runtime):**
- `<status-emoji>`: Status indicator (✅ ✨ 📝 ❌ 🔄 ↻ ⚠️ 🔍 📋 ✎)
- `<status-text>`: Status description (Completed, Created, Updated, Rejected, Superseded, Working)
- `<AgentName>`: AI's actual name (e.g., `OpenCode Desktop`, `OpenCode`)
- `<ModelID>`: Model identifier with provider (e.g., `ollama-cloud/glm-5`)

**⚠️ CRITICAL: NEVER copy example values literally. Detect your own identity.**

**Emoji Formatting:** Emoji must be PLAIN TEXT (NOT inside italic/bold formatting) to prevent render failures.

**Rule:** Byline = WHO did WHAT. Details belong in comment body, not byline. No extra context.

### Examples

**Task completion:**
```
<summary content>

---
🤖 ✅ Completed by <AgentName> (<ModelID>)
```

**Created issue:**
```markdown
[Issue body content]

---

> **Approval Tracking**: Approvals tracked via comments.

🤖 ✨ Created by <AgentName> (<ModelID>)
```

**Updated issue:**
```
🤖 ✨ Created by <AgentName> (<ModelID>)
🤖 📝 Updated by <AgentName> (<ModelID>)
```

**Rejected proposal:**
```
---
🤖 ❌ Rejected by <AgentName> (<ModelID>)
```

---

## Status Emoji Reference

| Status | Emoji | Byline Format |
|--------|-------|---------------|
| Task Complete | ✅ | `🤖 ✅ Completed by <AgentName> (<ModelID>)` |
| In Progress | ↻ | `🤖 ↻ Working by <AgentName> (<ModelID>)` |
| Created | ✨ | `🤖 ✨ Created by <AgentName> (<ModelID>)` |
| Updated | 📝 | `🤖 📝 Updated by <AgentName> (<ModelID>)` |
| Copy Editor | ✎ | `🤖 ✎ on behalf of <UserName>` |
| Completed | ✅ | `🤖 ✅ Completed by <AgentName> (<ModelID>)` |
| Rejected | ❌ | `🤖 ❌ Rejected by <AgentName> (<ModelID>)` |
| Superseded | 🔄 | `🤖 🔄 Superseded by <AgentName> (<ModelID>)` |
| Blocking | ⚠️ | `🤖 ⚠️ Blocking by <AgentName> (<ModelID>)` |
| Analysis | 🔍 | `🤖 🔍 Analysis by <AgentName> (<ModelID>)` |
| Decision | 📋 | `🤖 📋 Decision by <AgentName> (<ModelID>)` |

**Rule:** Byline = WHO did WHAT. Details belong in comment body, not byline.

---

## Copy Editor Byline (User-Authored Content)

### When to Use

Use the **Copy Editor** byline when posting content on behalf of users:
- User asks agent to investigate a codebase and post findings to GitHub
- User asks agent to analyze an issue and comment with results
- User requests agent to update an issue with investigation results
- Agent posts analysis, findings, or summaries on behalf of user

### When NOT to Use

Use standard bylines (Created, Completed, Updated) for:
- Agent creates its own spec/issue for implementation work
- Agent posts progress comments for its own implementation tasks
- Agent creates issues for user-approved specs (those already have user attribution)
- Agent performs independent implementation work

### Copy Editor Byline Format

**Format:**
```
<content posted on behalf of user>

---
🤖 ✎ on behalf of <UserName>
```

**Components:**
- `✎`: Pencil emoji indicates editing/posting role (not authorship)
- `on behalf of <UserName>`: The user who requested/owns the content

**Rule:** Byline = WHO did WHAT. Details belong in comment body, not byline.

### Examples

**Investigation Results Posted for User:**
```
## Analysis: Still an Issue (2026-04-01)

**Root Cause:** The `identifier` constraint in `Validations.scala` uses an overly restrictive regex pattern that rejects valid usernames containing hyphens.

**Location:** `Validations.scala#L16-L25`

**Recommendation:** Update regex to allow hyphens in username patterns.

---
🤖 ✎ on behalf of Michael Conrad
```

**Issue Comment Posted for User:**
```
## Status Update

Based on the investigation, the feature is ready for implementation. The API endpoints are designed and the database schema is finalized.

---
🤖 ✎ on behalf of Michael Conrad
```

---

## Issue/PR Body Attribution (Append Always)

**🚨 CRITICAL: ALWAYS APPEND. NEVER REPLACE.**

| Action | Operation | Byline |
|--------|-----------|--------|
| Create issue | Append | `🤖 ✨ Created by <AgentName> (<ModelID>)` |
| Update content | Append | `🤖 📝 Updated by <AgentName> (<ModelID>)` |
| Complete issue | Append | `🤖 ✅ Completed by <AgentName> (<ModelID>)` |
| Reject issue | Append | `🤖 ❌ Rejected by <AgentName> (<ModelID>)` |
| Supersede issue | Append | `🤖 🔄 Superseded by <AgentName> (<ModelID>)` |

**Rule:** Byline = WHO did WHAT. Details belong in comment body, not byline. No extra context.

**Why append-only:**
- Same rule everywhere (no confusion)
- Matches comment history behavior
- Preserves full lifecycle visibility
- No special cases to remember

**Example lifecycle (append-only):**
```markdown
[Issue body content]

---

> **Approval Tracking**: Approvals tracked via comments.

🤖 ✨ Created by <AgentName> (<ModelID>)
🤖 📝 Updated by <AgentName> (<ModelID>)
🤖 ✅ Completed by <AgentName> (<ModelID>)
```

---

## 🚫 CRITICAL VIOLATIONS (Zero Tolerance)

| Violation | Consequence |
|-----------|--------------|
| Missing progress comments after task completion | CRITICAL — implementation incomplete |
| Ignoring user comments without posting response | CRITICAL — user cannot see your reasoning |
| Closing issue without explanation comment | CRITICAL — no audit trail |
| Editing issue body to add "CLOSED" text | CRITICAL — destroys history |
| Proceeding to next task without posting comment | CRITICAL — breaks workflow |
| Using PREFIX for comment attribution | CRITICAL — wrong position |
| Replacing existing attribution (not appending) | CRITICAL — destroys history |
| Wrapping emoji in italic/bold | CRITICAL — render failure |

**See `github-comments` skill for:**
- Complete comment format rules
- Progress comment format and timing
- Issue body update rules
- Closure comment format
- When NOT to comment

---

## Integration with Guidelines

| Guideline | Section |
|-----------|---------|
| `120-github-issue-first.md` | Issue workflow, sub-issues |
| `000-critical-rules.md` | Critical violation enforcement |
| `github-comments` skill | Complete comment protocol |

---