# Release Notes: GitBucket 4.44.0

**Release Date:** 2025-09-23  
**Release Notes URL:** https://github.com/gitbucket/gitbucket/releases/tag/4.44.0

---

## Enhanced Branch Protection

GitBucket 4.44.0 introduces enhanced branch protection with the following new features:

### New Features

1. **Push Restrictions**: Repository administrators can now restrict push access to specific users
   - New `restrictions.users` field in branch protection API
   - Only listed users can push to protected branches
   - Works with status checks and enforcement settings

2. **Admin Enforcement**: New `enforce_admins` option
   - When enabled, branch protection rules apply to repository administrators
   - When disabled, administrators can bypass protection rules

### API Changes

**Breaking Changes:**
- Branch Protection API response schema changed
- Request schema for enabling protection updated
- New database tables and columns for restrictions

**Migration Required:**
- Clients reading branch protection must handle new `restrictions` and `enforce_admins` fields
- Clients updating protection must use new request schema
- See `api-diff.md` for detailed migration guide

---

## Other Changes

- Improved logging for initialization errors
- Various bug fixes and performance improvements

---

## Upgrade Notes

1. **Database Migration**: GitBucket will automatically create new tables on startup:
   - `PROTECTED_BRANCH_RESTRICTION` table
   - New columns in `PROTECTED_BRANCH`: `REQUIRED_STATUS_CHECK`, `RESTRICTIONS`

2. **API Compatibility**: This release includes breaking changes to the Branch Protection API
   - Update API clients to handle new schema
   - Test existing integrations before production deployment

3. **Backward Compatibility**: 
   - Existing branch protection rules will continue to work
   - New fields are optional in responses
   - Migration preserves existing protection settings

---

## Source Verification

This document was generated from direct source code analysis.
All API changes were verified against:
- GitBucket source code: https://github.com/gitbucket/gitbucket
- Release tag: 4.44.0
- Commit SHA: f661ee26d182b0a5cd60011fd61af2336311a94b

Release notes were verified against source code changes.