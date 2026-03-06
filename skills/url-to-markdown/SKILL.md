---
name: url-to-markdown
description: 将网页 URL 转换为 Markdown 文档并保存到本地。支持自动下载图片、美化格式、添加学习目标等内容增强。
---

# URL to Markdown

## 概述

将网页 URL 转换为清晰的 Markdown 文档，自动下载图片到本地并更新引用，同时添加学习目标、前置知识等内容增强。

## 使用方式

### 触发命令

```
/url-to-markdown <URL> [输出文件路径]
```

**示例**：
```
/url-to-markdown https://example.com/post/123
/url-to-markdown https://example.com/post/123 ./docs/article.md
```

## 工作原理

此技能通过 Claude Code 的智能处理 + Commands 脚本执行：

1. **Claude 智能思考**：分析网页内容，生成学习目标、前置知识、FAQ
2. **脚本执行**：获取网页内容、转换为 Markdown、下载图片、美化格式

## Claude 处理流程

当用户触发命令时，Claude 会：

1. **调用脚本**获取网页内容并转换为 Markdown
2. **读取并分析**生成的 Markdown 文档
3. **智能生成**：
   - 学习目标（4-6个，基于文档内容）
   - 前置知识（相关技术栈）
   - FAQ（如果是教程类型）
4. **插入内容**到文档开头
5. **执行脚本**下载图片和美化格式

## 功能说明

1. **网页获取**：从 URL 获取网页内容
2. **Markdown 转换**：将 HTML 转换为清晰的 Markdown 格式
3. **创建 img 文件夹**：在 Markdown 文件同目录下创建 `img` 文件夹
4. **下载图片**：提取并下载所有图片到 `img` 文件夹（使用 MD5 哈希命名）
5. **更新引用**：将图片引用更新为本地路径 `./img/filename.jpg`
6. **美化格式**：标题空行、列表规范化、删除多余空行等
7. **AI 内容增强**：Claude 智能生成学习目标、前置知识、FAQ（无需配置）

## 脚本说明

Commands 自动执行以下脚本：

```bash
# 1. 获取网页并转换为 Markdown
python3 ${CLAUDE_PLUGIN_ROOT}/skills/url-to-markdown/scripts/url_to_markdown.py <URL> [输出文件路径]

# 2. 增强内容（添加学习目标、前置知识等）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/enhance_content.py --enhance <输出文件路径>
```

## 依赖

```bash
pip install requests beautifulsoup4 html2text
```

## 手动运行脚本

```bash
# 脚本位置
ls -la skills/url-to-markdown/scripts/

# 方式1：完整流程（转换 + 增强）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/url-to-markdown/scripts/url_to_markdown.py <URL> [输出文件路径]
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/enhance_content.py --enhance <输出文件路径>

# 方式2：仅转换网页
python3 ${CLAUDE_PLUGIN_ROOT}/skills/url-to-markdown/scripts/url_to_markdown.py <URL> [输出文件路径]
```
