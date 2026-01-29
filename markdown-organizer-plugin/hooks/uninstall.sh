#!/usr/bin/env bash
# Cleanup hook for markdown-organizer plugin
# Removes skill files when the plugin is uninstalled

set -euo pipefail

SKILL_DEST="${HOME}/.claude/skills/markdown-organizer"

echo "🗑️  Uninstalling markdown-organizer plugin..."

# Remove skill files if they exist
if [ -d "${SKILL_DEST}" ]; then
    echo "Removing skill files from ${SKILL_DEST}..."
    rm -rf "${SKILL_DEST}"

    if [ $? -eq 0 ]; then
        echo "✅ Skill files removed successfully!"
    else
        echo "⚠️  Failed to remove skill files. Please remove manually:"
        echo "   rm -rf ${SKILL_DEST}"
    fi
else
    echo "ℹ️  Skill files not found, nothing to remove."
fi

echo "✅ Uninstallation complete!"

exit 0