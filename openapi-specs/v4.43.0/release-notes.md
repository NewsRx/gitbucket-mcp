# GitBucket Release Notes - Version 4.43.0

**Release Date:** 2025-06-29  
**Release Tag:** 4.43.0  
**Release URL:** https://github.com/gitbucket/gitbucket/releases/tag/4.43.0

---

## Summary

GitBucket 4.43.0 is a **backend maintenance release** with NO API changes.

### Key Change

- **H2 Database Upgrade**: H2 database upgraded from 1.x to 2.x

### Impact

- **API**: No changes - all endpoints remain compatible
- **Schema**: No changes - all request/response formats unchanged
- **Authentication**: No changes - all auth mechanisms unchanged

---

## ⚠️ Breaking Change for H2 Users

Users with H2 databases (:warning: **BREAKING**) must perform manual migration before upgrading.

### Migration Required

```bash
# Export database using H2 1.4.199
curl -O https://repo1.maven.org/maven2/com/h2database/h2/1.4.199/h2-1.4.199.jar
java -cp h2-1.4.199.jar org.h2.tools.Script \
    -url "jdbc:h2:~/.gitbucket/data" \
    -user sa -password sa \
    -script dump.sql

# Recreate database using H2 2.3.232
curl -O https://repo1.maven.org/maven2/com/h2database/h2/2.3.232/h2-2.3.232.jar
java -cp h2-2.3.232.jar org.h2.tools.RunScript \
    -url "jdbc:h2:~/.gitbucket/data" \
    -user sa -password sa \
    -script dump.sql
```

### Configuration Update

If `~/.gitbucket/database.conf` contains `;MVCC=true` in the connection URL, remove it:

```
db {
  url = "jdbc:h2:${DatabaseHome};MVCC=true" // => "jdbc:h2:${DatabaseHome}"
  ...
}
```

---

## Non-Affected Users

**PostgreSQL and MySQL users are NOT affected.**

No migration required. Upgrade directly to 4.43.0.

---

## API Compatibility

| Aspect | Compatibility |
|--------|---------------|
| Endpoint Count | ✅ Unchanged (93 endpoints) |
| Endpoint Paths | ✅ Unchanged |
| Request Schemas | ✅ Unchanged |
| Response Schemas | ✅ Unchanged |
| Authentication | ✅ Unchanged |

**External API clients require NO changes.**

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| `openapi.json` | Full OpenAPI 3.0.3 specification |
| `api-diff.md` | API differences from v4.42.1 |
| This file (`release-notes.md`) | Official release notes |

---

*Release notes for GitBucket 4.43.0*