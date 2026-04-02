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

- **AI Agent Configuration** - Complete OpenCode Desktop configuration for GitBucket MCP development with 25+ guideline files, 16 skill modules, git hooks, and utility scripts. Developers can now use AI agents with proper context isolation and workflow enforcement.
- **Upstream Release Detection** - GitHub Actions workflow automatically detects new GitBucket releases and creates issues for spec updates. Detects stable releases, filters pre-releases, and tracks state across runs.
- **Language-Agnostic Release Template** - Release detection template works for any programming language by discovering directory structure dynamically instead of hardcoding paths. CHANGELOGs and migration guides are treated as untrusted—only source diffs are authoritative.
- **Git Commit Analysis Pattern** - Sub-task execution pattern isolates skill thinking tokens from main context. When generating changelogs, the skill analyzes commits in isolation and returns minimal result tokens.

### Changed

- **Git Stash Workflow** - Enforced mandatory `git stash -u` before branch operations to prevent data loss. The `-u` flag ensures untracked files are preserved when switching branches.
- **Branch-First Enforcement** - All state file updates now require full PR workflow (branch, commit with trailers, push, PR creation). Direct commits to workflow state files are now blocked by guidelines.
- **Executive Summary Format** - Chat outputs now require executive summary BEFORE URL. Context is provided before the clickable link, improving communication clarity.
- **OpenAPI Spec Generation** - Source-first analysis workflow prioritizes code diffs over CHANGELOGs. Discovered breaking API changes in GitBucket 4.42.1 that were undocumented in official release notes.

### Fixed

- **Workflow YAML Parse Error** - Fixed heredoc construction in GitHub Actions workflow that caused YAML parse failures. Template file approach replaces fragile heredoc syntax.
- **Analysis Authorization Gap** - Documented critical violation for implementing during analysis without explicit authorization. "Check error" now means read logs only, not fix and create PR.
- **PR Timing Violations** - Documented that "approved" authorizes implementation only—PR creation requires explicit "create a PR" instruction after developer testing.

---

## [0.0.1] - 2026-04-01

### Added

- **AI Agent Guidelines** - 25+ guideline files covering git workflow, GitHub operations, planning methodology, error handling, and code standards. Guidelines enforce zero-tolerance rules for data loss, scope creep, and context pollution.
- **Skill Module Architecture** - 16 skill modules with sub-task support for context-efficient execution. Skills can be invoked with `--task` parameter to load only specific workflow phases.
- **Git Hooks** - Pre-commit hook blocks commits to main branch, post-commit hook warns after commits to main. Enforces branch-first workflow.
- **OpenAPI Baseline** - GitBucket 4.40.0 OpenAPI specification documenting 93 API endpoints across users, repositories, issues, pull requests, and more.
- **Copy Editor Byline** - AI agents can post content on behalf of users with `🤖 ✎ on behalf of <UserName>` attribution. Used for investigation results, analysis summaries, and user-authored content.

### Fixed

- **Session Init Field Names** - Fixed `GIT_USER_NAME`/`GIT_USER_EMAIL` to `DEV_NAME`/`DEV_EMAIL` to distinguish developer info from repository info.
- **Initial Project Setup** - Added .gitignore for Python projects (bytecode, venv, IDE configs, temp files).

---

[Unreleased]: https://github.com/NewsRx/gitbucket-mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/NewsRx/gitbucket-mcp/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/NewsRx/gitbucket-mcp/commits/v0.0.1