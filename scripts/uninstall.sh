#!/bin/bash
set -e

echo "=== Markdown Organizer 卸载功能 ==="

# 1. 检测并删除技能文件
COMMAND_FILE="$HOME/.claude/commands/markdown-organizer.md"
if [ -f "$COMMAND_FILE" ]; then
    echo "删除技能命令文件: $COMMAND_FILE"
    rm "$COMMAND_FILE"
else
    echo "未找到技能命令文件: $COMMAND_FILE"
fi

# 2. 检测并删除技能目录
SKILL_DIR="$HOME/.claude/skills/markdown-organizer"
if [ -d "$SKILL_DIR" ]; then
    echo "删除技能目录: $SKILL_DIR"
    rm -rf "$SKILL_DIR"
else
    echo "未找到技能目录: $SKILL_DIR"
fi

# 3. 卸载 pip 依赖
echo "卸载 pip 依赖: requests"
pip3 uninstall -y requests 2>/dev/null || echo "requests 未安装或卸载失败"

echo "=== 卸载完成 ==="
