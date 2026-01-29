#!/usr/bin/env bash
# Setup hook for markdown-organizer plugin
# Automatically installs Python dependencies and copies skill files when the plugin is installed

set -euo pipefail

# Determine plugin root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_SOURCE="${PLUGIN_ROOT}/skills/markdown-organizer"
SKILL_DEST="${HOME}/.claude/skills/markdown-organizer"

echo "📦 Installing markdown-organizer plugin..."

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "⚠️  pip not found. Please install Python and pip manually."
    echo "   Run: pip install requests"
else
    # Install requests library
    echo "Installing requests library..."
    pip install requests

    if [ $? -eq 0 ]; then
        echo "✅ Dependencies installed successfully!"
    else
        echo "⚠️  Failed to install dependencies. Please run manually:"
        echo "   pip install requests"
    fi
fi

# Copy skill files to Claude skills directory
echo ""
echo "📁 Copying skill files to ${SKILL_DEST}..."

# Create destination directory if it doesn't exist
mkdir -p "${HOME}/.claude/skills"

# Remove existing skill directory if it exists
if [ -d "${SKILL_DEST}" ]; then
    echo "Removing existing skill directory..."
    rm -rf "${SKILL_DEST}"
fi

# Copy skill files
cp -r "${SKILL_SOURCE}" "${SKILL_DEST}"

if [ $? -eq 0 ]; then
    echo "✅ Skill files copied successfully!"
else
    echo "⚠️  Failed to copy skill files. Please run manually:"
    echo "   cp -r ${SKILL_SOURCE} ${SKILL_DEST}"
fi

echo ""
echo "✅ Installation complete!"

exit 0
