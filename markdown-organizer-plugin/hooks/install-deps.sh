#!/usr/bin/env bash
# Setup hook for markdown-organizer plugin
# Automatically installs Python dependencies when the plugin is installed

set -euo pipefail

# Determine plugin root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "📦 Installing markdown-organizer dependencies..."

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "⚠️  pip not found. Please install Python and pip manually."
    echo "   Run: pip install requests"
    exit 0
fi

# Install requests library
echo "Installing requests library..."
pip install requests

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "⚠️  Failed to install dependencies. Please run manually:"
    echo "   pip install requests"
fi

exit 0
