#!/bin/bash
# 检查插件更新脚本
# 在 Claude Code 会话启动时运行

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT}"
CURRENT_VERSION=$(cat "$PLUGIN_ROOT/.claude-plugin/plugin.json" | grep '"version"' | sed 's/.*: *"\([^"]*\)".*/\1/')
REPO_URL=$(cat "$PLUGIN_ROOT/.claude-plugin/plugin.json" | grep '"repository"' | sed 's/.*: *"\([^"]*\)".*/\1/')

# 提取 owner 和 repo
OWNER_REPO=$(echo "$REPO_URL" | sed 's|https://github.com/||' | sed 's|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d'/' -f1)
REPO=$(echo "$OWNER_REPO" | cut -d'/' -f2)

# 获取 GitHub 最新 release 版本
LATEST_TAG=$(git ls-remote --tags "https://github.com/$OWNER_REPO.git" 2>/dev/null | grep 'refs/tags/v[0-9]' | awk '{print $2}' | sed 's|refs/tags/||' | sort -V | tail -1)

if [ -z "$LATEST_TAG" ]; then
    # 无法获取远程版本，跳过检查
    exit 0
fi

# 移除 v 前缀进行版本比较
CURRENT_NUM=$(echo "$CURRENT_VERSION" | sed 's/v//')
LATEST_NUM=$(echo "$LATEST_TAG" | sed 's/v//')

# 版本比较
if [ "$CURRENT_NUM" != "$LATEST_NUM" ]; then
    echo "📦 插件更新可用: $CURRENT_VERSION → $LATEST_TAG"
    echo "运行 /plugin update organize_markdown@markdown-organizer 更新"
    echo ""
fi
