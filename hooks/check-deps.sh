#!/usr/bin/env bash
# Dependency check hook for markdown-organizer plugin
# Checks if Python dependencies are installed, auto-installs if missing

set -euo pipefail

# Only check if pip is available and dependencies are not installed
if command -v pip &> /dev/null; then
    MISSING_DEPS=()

    # Check if requests is installed
    if ! pip show requests &> /dev/null; then
        MISSING_DEPS+=("requests")
    fi

    # Check if beautifulsoup4 is installed
    if ! pip show beautifulsoup4 &> /dev/null; then
        MISSING_DEPS+=("beautifulsoup4")
    fi

    # Check if html2text is installed
    if ! pip show html2text &> /dev/null; then
        MISSING_DEPS+=("html2text")
    fi

    # Check if markdown is installed (for wechat-format)
    if ! pip show markdown &> /dev/null; then
        MISSING_DEPS+=("markdown")
    fi

    if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
        echo "🔍 markdown-organizer: 检测到缺失的 Python 依赖: ${MISSING_DEPS[*]}"
        echo "⚙️  正在自动安装..."
        pip install -i https://pypi.tuna.tsinghua.edu.cn/simple "${MISSING_DEPS[@]}"
        echo "✅ 依赖安装完成!"
    else
        echo "✅ markdown-organizer: 所有依赖已安装"
    fi
else
    echo "⚠️  markdown-organizer: pip 未找到"
    echo "   请先安装 Python 和 pip，然后手动运行: pip install requests beautifulsoup4 html2text markdown"
fi

exit 0
