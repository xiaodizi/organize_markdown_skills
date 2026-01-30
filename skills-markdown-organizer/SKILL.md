---
name: markdown-organizer
description: 组织和美化 Markdown 文档，自动下载图片到本地。用于处理从网页复制的 markdown 文件。
disable-model-invocation: true
allowed-tools: Bash(python3 *)
---

# Markdown Organizer

组织和美化从网页复制的 Markdown 文档。

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

1. **图片本地化**：自动下载 Markdown 中的图片到 `img` 文件夹
2. **路径更新**：将图片引用从网络 URL 更新为本地路径
3. **格式美化**：
   - 标题前后添加空行
   - 统一列表标记为 `- `
   - 规范化代码块
   - 删除多余空行
   - 去除行尾空格

## 依赖

```bash
pip install requests
```
