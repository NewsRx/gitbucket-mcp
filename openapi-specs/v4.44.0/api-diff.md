# API Differences: GitBucket 4.43.0 → 4.44.0

**Source Analysis Date:** 2026-04-03  
**Analysis Method:** Direct source code comparison between 4.43.0 and 4.44.0  
**Source Repository:** https://github.com/gitbucket/gitbucket

---

## Summary

GitBucket 4.44.0 introduces **branch protection enhancements** with breaking changes to the Branch Protection API. The API now supports restricting push access to specific users and has a new `enforce_admins` field.

---

## Breaking Changes

### 1. Branch Protection API Schema Change

**Endpoints Affected:**
- `GET /repos/{owner}/{repo}/branches/{branch}/protection`
- `GET /repos/{owner}/{repo}/branches/{branch}`
- `PUT /repos/{owner}/{repo}/branches/{branch}/protection`

**Breaking Change:** Response schema changed from `ApiBranchProtection` to `ApiBranchProtectionResponse`

**Old Schema (4.43.0):**
```json
{
  "url": "string",
  "enabled": true,
  "required_status_checks": {
    "url": "string",
    "enforcement_level": "off|non_admins|everyone",
    "contexts": ["string"],
    "contexts_url": "string"
  }
}
```

**New Schema (4.44.0):**
```json
{
  "url": "string",
  "enabled": true,
  "required_status_checks": {
    "url": "string",
    "enforcement_level": "off|non_admins|everyone",
    "contexts": ["string"],
    "contexts_url": "string"
  },
  "restrictions": {
    "users": ["string"]
  },
  "enforce_admins": {
    "enabled": true
  }
}
```

**New Fields:**
- `restrictions` - Optional object containing push access restrictions
  - `users` - Array of usernames allowed to push to this branch
- `enforce_admins` - Optional object (only present when protection enabled)
  - `enabled` - Boolean indicating if admins are subject to branch protection rules

**Schema Changes:**
1. Response type renamed from `ApiBranchProtection` to `ApiBranchProtectionResponse`
2. New request schema: `ApiBranchProtectionRequest` for PUT operations
3. New database table: `PROTECTED_BRANCH_RESTRICTION` for user restrictions

---

## New Endpoints

None. All existing endpoints remain unchanged in path.

---

## Modified Endpoints

### 1. PUT /repos/{owner}/{repo}/branches/{branch}/protection

**Request Body Changes:**

**Old Request (4.43.0):**
```json
{
  "protection": {
    "enabled": true,
    "status": {
      "enforcement_level": "everyone",
      "contexts": ["ci/travis"]
    }
  }
}
```

**New Request (4.44.0):**
```json
{
  "protection": {
    "enabled": true,
    "required_status_checks": {
      "contexts": ["ci/travis"]
    },
    "restrictions": {
      "users": ["username1", "username2"]
    },
    "enforce_admins": true
  }
}
```

**Request Schema Changes:**
- Field `status.enforcement_level` removed (no longer a request field)
- New field `enforce_admins` - Boolean to enforce protection rules on repository admins
- New field `restrictions.users` - Array of usernames allowed to push
- Field `required_status_checks` replaces `status` object
- Field `required_status_checks.contexts` - Status check contexts required before merging

**Database Changes:**
- New table: `PROTECTED_BRANCH_RESTRICTION`
  - Columns: `USER_NAME`, `REPOSITORY_NAME`, `BRANCH`, `ALLOWED_USER`
- New columns in `PROTECTED_BRANCH`:
  - `REQUIRED_STATUS_CHECK` (Boolean)
  - `RESTRICTIONS` (Boolean)
- Column renamed: `STATUS_CHECK_ADMIN` → `ENFORCE_ADMINS` (same semantics, new name)

---

### 2. GET /repos/{owner}/{repo}/branches/{branch}

**Response Schema Changes:**

The response for branch information now includes the new protection schema:

**Field Path:** `protection` object

- Type changed from `ApiBranchProtection` to `ApiBranchProtectionResponse`
- New sub-field: `enforce_admins`
- New sub-field: `restrictions`

---

### 3. GET /repos/{owner}/{repo}/branches/{branch}/protection

**Response Body:** Same breaking changes as documented for the `protection` field in branch GET endpoint.

---

## Deprecated Endpoints

None in this release.

---

## Removed Endpoints

None in this release.

---

## Internal Changes (No API Impact)

The following internal changes were made but do not affect the external API:

1. **Code Refactoring:** Branch protection model classes renamed
   - `ApiBranchProtection` → `ApiBranchProtectionResponse` (for API responses)
   - `ApiBranchProtectionRequest` (new, for API requests)
   - `ApiBranchProtection.EnablingAndDisabling` → `ApiBranchProtectionRequest.EnablingAndDisabling`

2. **Service Layer:** `ProtectedBranchService.ProtectedBranchInfo` constructor updated
   - New parameter: `restrictionsUsers: Option[Seq[String]]`
   - Parameter renamed: `includeAdministrators` → `enforceAdmins`
   - Parameter changed: `contexts: Seq[String]` → `contexts: Option[Seq[String]]`

3. **Model Layer:** `ProtectedBranch` case class updated
   - New fields: `requiredStatusCheck: Boolean`, `restrictions: Boolean`
   - Renamed field: `statusCheckAdmin` → `enforceAdmins`

4. **Migration:** Database migration added for new columns and tables
   - File: `src/main/resources/update/gitbucket-core_4.44.xml`

---

## Error Handling Changes

### New Error Condition

**Endpoint:** `PUT /repos/{owner}/{repo}/branches/{branch}/protection`

**New Error:** When `restrictions.users` contains invalid usernames:
- HTTP Status: 422 Unprocessable Entity
- Condition: User does not exist or lacks push access to repository

---

## Authentication Changes

None. Authentication requirements remain unchanged.

---

## Verification Against Release Notes

**Release Notes Claimed:**
> Enhanced branch protection which supports the following settings:
> - Prevent pushes from non-allowed users
> - Whether to apply restrictions to administrator users as well

**Source Verification:** ✅ CONFIRMED

Source analysis confirms:
1. ✅ New `restrictions.users` field for push access control
2. ✅ New `enforce_admins` field for admin protection rules
3. ✅ Database changes support user-specific push restrictions
4. ✅ Service layer validates and enforces user restrictions

**Release Notes Accuracy:** The release notes accurately describe the branch protection enhancement. No discrepancies found.

---

## Migration Guide for API Consumers

### For Clients Reading Branch Protection

**Before (4.43.0):**
```bash
curl -H "Authorization: token $TOKEN" \
  https://gitbucket.example.com/api/v3/repos/owner/repo/branches/main/protection
```

**Response schema changed:** Update client to handle:
- `restrictions.users` array (may be null)
- `enforce_admins.enabled` boolean (may be null)

### For Clients Updating Branch Protection

**Before (4.43.0):**
```json
{
  "protection": {
    "enabled": true,
    "status": {
      "enforcement_level": "everyone",
      "contexts": ["ci/travis"]
    }
  }
}
```

**After (4.44.0):**
```json
{
  "protection": {
    "enabled": true,
    "required_status_checks": {
      "contexts": ["ci/travis"]
    },
    "enforce_admins": true,
    "restrictions": {
      "users": ["allowed-user"]
    }
  }
}
```

**Migration Steps:**
1. Remove `status.enforcement_level` from requests (no longer used)
2. Move `contexts` to `required_status_checks.contexts`
3. Add `enforce_admins` to control admin restriction
4. Add `restrictions.users` to limit push access (optional)

---

## Files Changed

**API Models:**
- `src/main/scala/gitbucket/core/api/ApiBranch.scala` - Updated `protection` type
- `src/main/scala/gitbucket/core/api/ApiBranchProtection.scala` - Renamed to `ApiBranchProtectionResponse.scala`
- `src/main/scala/gitbucket/core/api/ApiBranchProtectionRequest.scala` - NEW FILE
- `src/main/scala/gitbucket/core/api/JsonFormat.scala` - Updated serializers

**Controllers:**
- `src/main/scala/gitbucket/core/controller/api/ApiRepositoryBranchControllerBase.scala` - Updated handling
- `src/main/scala/gitbucket/core/controller/api/ApiRepositoryContentsControllerBase.scala` - Path fix

**Database:**
- `src/main/scala/gitbucket/core/model/ProtectedBranch.scala` - New fields, new table
- `src/main/scala/gitbucket/core/service/ProtectedBranchService.scala` - Updated service logic
- `src/main/resources/update/gitbucket-core_4.44.xml` - Migration script

---

## Testing Recommendations

When testing against GitBucket 4.44.0:

1. **Test branch protection with user restrictions:**
   - Create a branch protection rule with `restrictions.users`
   - Verify only listed users can push
   - Verify admin override behavior with `enforce_admins`

2. **Test backward compatibility:**
   - Verify old clients receive new fields gracefully
   - Verify `null` handling for optional fields

3. **Test edge cases:**
   - Empty `restrictions.users` array (no users allowed)
   - `enforce_admins: false` vs `enforce_admins: true`
   - Status checks with and without restrictions