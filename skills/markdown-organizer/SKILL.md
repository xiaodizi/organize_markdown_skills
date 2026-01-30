---
name: markdown-organizer
description: Markdown 文档组织和美化工具。用于处理从网页复制的 markdown 文件：下载图片到本地 img 文件夹、更新图片引用为本地路径、美化 markdown 格式。支持通过 `/markdown-organizer @文件路径` 命令触发。
---

# Markdown Organizer

## 概述

组织和美化从网页复制的 markdown 文件，自动下载图片到本地并更新引用。

## 使用方式

### 触发命令

```
/markdown-organizer @文件路径 [base_url]
```

**示例**：
```
/markdown-organizer @/Users/lei.fu/documents/article.md
/markdown-organizer @article.md https://example.com/post/123
```

## 工作原理

此技能通过 Commands 执行脚本。Claude Code 会自动解析 `{skill_dir}` 变量为插件安装路径。

**执行流程**：
1. 用户触发 `/markdown-organizer @文件路径`
2. Claude 解析 `{skill_dir}` 为插件缓存目录
3. 运行：`python3 {skill_dir}/scripts/organize_markdown.py <文件路径>`

## 功能说明

1. **创建 img 文件夹**：在 markdown 文件同目录下创建 `img` 文件夹
2. **下载图片**：提取并下载所有图片到 `img` 文件夹（使用 MD5 哈希命名）
3. **更新引用**：将图片引用更新为本地路径 `./img/filename.jpg`
4. **美化格式**：标题空行、列表规范化、删除多余空行等

## 依赖

```bash
pip install requests
```

## 手动运行脚本

如果需要手动运行脚本：

```bash
# 查找脚本位置
ls -la ~/.claude/plugins/cache/markdown-organizer/markdown-organizer/*/scripts/

# 运行
python3 ~/.claude/plugins/cache/markdown-organizer/markdown-organizer/<commit>/scripts/organize_markdown.py <文件路径> [base_url]
```
