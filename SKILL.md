---
name: organize_markdown
description: 组织和美化 markdown 文档，自动下载图片到本地 img 文件夹，支持 URL 直接转换为 Markdown
version: 1.0.8
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

- **Web Clipper 支持**：自动处理 Obsidian Web Clipper 元数据，合并 frontmatter，从 title 字段生成一级标题
- 自动下载图片到本地 `img` 文件夹
- 更新图片引用为本地路径
- 美化 Markdown 格式（标题空行、列表规范化等）
- 基于文档内容自动生成：摘要、学习目标、知识图谱、FAQ
- 支持相对路径图片处理（通过 base_url 参数）
- 修复 YAML frontmatter 缩进问题
- 保证输出文档末尾换行，避免标题渲染异常

## 执行流程（Gemini CLI / Claude Code）

### markdown-organizer

```bash
# 0) Claude 处理 Web Clipper 元数据（可选）
# - 提取并合并 frontmatter 属性
# - 从 title 字段生成文档标题
# - 清理重复的元数据

# 1) Claude 按步骤执行：
# - 分析文档内容
# - 生成摘要、学习目标、知识图谱、FAQ
# - 插入到文档顶部

# 2) 处理图片和格式
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py <文件路径> [base_url]

# 3) Claude 验证并生成完成报告
```

### url-to-markdown

```bash
# 1) URL 转 Markdown（含图片下载和格式美化）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/url-to-markdown/scripts/url_to_markdown.py <URL> [输出文件路径]

# 2) Claude 按步骤执行：
# - 分析文档内容
# - 生成摘要、学习目标、前置知识、FAQ
# - 插入到文档顶部

# 3) Claude 检查和保存
```
