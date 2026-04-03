# GitBucket 4.45.0 Release Notes

**Release Date:** 2026-01-10  
**Release Tag:** 4.45.0  
**Upstream Release:** https://github.com/gitbucket/gitbucket/releases/tag/4.45.0

---

## Overview

GitBucket 4.45.0 is a **UI-focused release** with no API changes from 4.44.0.

---

## Changes

### New Features

1. **Show Full Username on UI**
   - New option to display full usernames in the interface
   - API Impact: None (UI-only change)

2. **Render Plugin Support**
   - Plugins can now render content in issues, pull requests, wiki, and commit comments
   - Extensions to existing render hooks
   - API Impact: None (server-side rendering)

3. **Wiki Link Syntax**
   - Support for linking to other pages from Wiki using Wiki link syntax
   - API Impact: None (Wiki parsing change)

---

## API Impact Summary

| Category | Status |
|----------|--------|
| New Endpoints | None |
| Modified Endpoints | None |
| Removed Endpoints | None |
| Schema Changes | None |
| Authentication Changes | None |
| Breaking Changes | None |

**Conclusion:** This release has **zero API impact**. All existing API integrations continue to work without modification.

---

## Migration Notes

**No migration required for API consumers.**

Clients using GitBucket 4.44.0 can upgrade to 4.45.0 with no changes to API integration code.

---

## Version Compatibility

| Version | API Changes |
|---------|------------|
| 4.45.0 | None (UI-only release) |
| 4.44.0 | Branch protection schema changed |
| 4.43.0 | No changes |
| 4.42.1 | No changes |
| 4.42.0 | No changes |

---

## References

- **Source Diff:** https://github.com/gitbucket/gitbucket/compare/4.44.0...4.45.0
- **OpenAPI Spec:** `openapi.json` (this directory)
- **API Diff:** `api-diff.md` (this directory)
- **Agent Reference:** `AGENTS.md` (this directory)