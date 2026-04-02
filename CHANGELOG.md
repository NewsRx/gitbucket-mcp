# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Changelog Generator Skill Integration** - Automated CHANGELOG.md updates during PR creation workflow. The skill runs as a sub-task to prevent context pollution from its git commit analysis and formatting operations.

### Changed

- **PR Workflow Enhanced** - Added `/skill changelog-generator` invocation to PR creation workflow. Changelog changes are now automatically included in the same commit as code changes via squash.

---

## [0.1.0] - 2026-04-02

### Added

- **Context Isolation** - Sub-task execution pattern ensures skill thinking tokens don't pollute main session context
- **Changelog Skill Import** - Imported changelog-generator from awesome-opencode-skills repository with full skill structure (SKILL.md, tasks/, reference/)
- **PR Workflow Integration** - Updated git-workflow pr-creation task to invoke changelog skill before squash
- **Skip Directive** - Added `[skip changelog]` directive support for PRs that don't need changelog updates
- **CHANGELOG.md** - Initial changelog file with Keep a Changelog format

[Unreleased]: https://github.com/NewsRx/gitbucket-mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/NewsRx/gitbucket-mcp/releases/tag/v0.1.0