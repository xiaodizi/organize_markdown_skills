#!/usr/bin/env bash
# Dependency check hook for markdown-organizer plugin
# Checks if Python dependencies are installed, prompts user if needed

set -euo pipefail

# Only check if pip is available and dependencies are not installed
if command -v pip &> /dev/null; then
    MISSING_DEPS=()

    # Check if requests is installed
    if ! pip show requests &> /dev/null; then
        MISSING_DEPS+=("requests")
    fi

    # Check if beautifulsoup4 is installed (optional but recommended)
    if ! pip show beautifulsoup4 &> /dev/null; then
        MISSING_DEPS+=("beautifulsoup4")
    fi

    # Check if html2text is installed (optional but recommended)
    if ! pip show html2text &> /dev/null; then
        MISSING_DEPS+=("html2text")
    fi

    if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
        echo "⚠️  markdown-organizer: Missing Python dependencies: ${MISSING_DEPS[*]}"
        echo "   Please run: pip install ${MISSING_DEPS[*]}"
    fi
else
    echo "⚠️  markdown-organizer: pip not found."
    echo "   Please install Python and pip, then run: pip install requests beautifulsoup4 html2text"
fi

exit 0
