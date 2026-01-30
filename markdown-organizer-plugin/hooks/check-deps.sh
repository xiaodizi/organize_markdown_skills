#!/usr/bin/env bash
# Dependency check hook for markdown-organizer plugin
# Checks if Python dependencies are installed, prompts user if needed

set -euo pipefail

# Only check if pip is available and requests is not installed
if command -v pip &> /dev/null; then
    # Check if requests is installed
    if ! pip show requests &> /dev/null; then
        echo "⚠️  markdown-organizer: Python 'requests' library not found."
        echo "   Please run: pip install requests"
    fi
else
    echo "⚠️  markdown-organizer: pip not found."
    echo "   Please install Python and pip, then run: pip install requests"
fi

exit 0
