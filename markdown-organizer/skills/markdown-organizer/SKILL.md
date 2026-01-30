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
/markdown-organizer @<文件路径>
```

### 脚本路径

**请使用以下命令查找脚本位置**：
```bash
ls -la ~/.claude/plugins/cache/markdown-organizer/markdown-organizer/*/scripts/organize_markdown.py
```

**运行格式**：
```bash
python3 ~/.claude/plugins/cache/markdown-organizer/markdown-organizer/<commit>/scripts/organize_markdown.py <文件路径> [base_url]
```

其中 `<commit>` 是安装时的 git commit 哈希值（如 `599dee49cc81`）。

### 参数说明

- `<文件路径>`: Markdown 文件路径（必需）
- `[base_url]`: 原文章页面的 URL（可选，用于解析相对路径的图片）

### 示例

```bash
# 基本使用
python3 ~/.claude/plugins/cache/markdown-organizer/markdown-organizer/599dee49cc81/scripts/organize_markdown.py article.md

# 带源 URL（处理相对路径图片）
python3 ~/.claude/plugins/cache/markdown-organizer/markdown-organizer/599dee49cc81/scripts/organize_markdown.py article.md https://example.com/post/123
```

## 功能说明

1. **创建 img 文件夹**：在 markdown 文件同目录下创建 `img` 文件夹
2. **下载图片**：提取并下载所有图片到 `img` 文件夹（使用 MD5 哈希命名）
3. **更新引用**：将图片引用更新为本地路径
4. **美化格式**：标题空行、列表规范化、删除多余空行等

## 依赖

```bash
pip install requests
```
