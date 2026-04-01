#!/bin/bash
# Install git hooks to prevent commits to main branch
# This is a CRITICAL enforcement mechanism for the feature-branch workflow

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
HOOKS_DIR="$PROJECT_ROOT/.githooks"

echo "Installing git hooks..."

# Configure git to use .githooks directory
git config core.hooksPath ".githooks"

# Verify hooks are installed
HOOKS_PATH=$(git config core.hooksPath)
if [ "$HOOKS_PATH" = ".githooks" ]; then
    echo "✓ Git hooks path configured: .githooks"
else
    echo "✗ Failed to configure git hooks path"
    exit 1
fi

# Verify hooks are executable
for hook in pre-commit post-commit; do
    if [ -x "$HOOKS_DIR/$hook" ]; then
        echo "✓ $hook hook is executable"
    else
        echo "✗ $hook hook is not executable"
        chmod +x "$HOOKS_DIR/$hook"
        echo "  Fixed: made $hook executable"
    fi
done

echo ""
echo "Git hooks installed successfully!"
echo ""
echo "Enforcement:"
echo "  ✗ Commits to 'main' branch BLOCKED (pre-commit)"
echo "  ⚠  Commits to 'main' WARNED (post-commit backup)"
echo "  🤖 AI agent detection ENABLED"
echo ""
echo "To bypass (NOT RECOMMENDED):"
echo "  git commit --no-verify"
echo ""
echo "⚠️  WARNING: Bypassing hooks violates the feature-branch workflow."
echo "   See .opencode/guidelines/110-git-branch-first.md"