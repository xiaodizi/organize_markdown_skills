---
name: organize_markdown
description: 组织和美化 markdown 文档，自动下载图片到本地 img 文件夹，支持 URL 直接转换为 Markdown
version: 1.0.6
author:
  name: lei.fu
keywords: ["markdown", "organize", "images", "beautify", "url", "webpage"]
homepage: https://github.com/xiaodizi/organize_markdown_skills
repository: https://github.com/xiaodizi/organize_markdown_skills.git
---

# Organize Markdown Skills

## 概述

这个插件提供了两个主要功能：

1. **Markdown Organizer**：组织和美化从网页复制的 markdown 文件，自动下载图片到本地并更新引用
2. **URL to Markdown**：将网页 URL 转换为 Markdown 文档并保存到本地

## 使用方式

### Markdown Organizer
```
/markdown-organizer @文件路径 [base_url]
```

### URL to Markdown
```
/url-to-markdown <URL> [输出文件路径]
```

## 功能特性

- 自动下载图片到本地 `img` 文件夹
- 更新图片引用为本地路径
- 美化 Markdown 格式（标题空行、列表规范化等）
- AI 智能生成学习目标、前置知识、FAQ
- 支持相对路径图片处理（通过 base_url 参数）