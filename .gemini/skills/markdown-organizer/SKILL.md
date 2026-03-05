---
name: markdown-organizer
description: Markdown 文档组织和美化工具。用于处理从网页复制的 markdown 文件：下载图片到本地 img 文件夹、更新图片引用为本地路径、美化 markdown 格式。支持通过自然语言或指定命令触发。
---

# Markdown Organizer

## 概述

组织和美化从网页复制的 markdown 文件，自动下载图片到本地并更新引用。

## 使用方式

### 触发命令

```
organize-markdown @文件路径 [base_url]
```

**示例**：
```
organize-markdown @/Users/lei.fu/documents/article.md
organize-markdown @article.md https://example.com/post/123
```

**自然语言触发**：
- "帮我美化这个 markdown 文档"
- "处理这个从网页复制的 markdown 文件"

## 工作原理

此技能通过 Gemini CLI 的智能处理 + Scripts 脚本执行：

1. **智能分析**：读取文档内容，生成学习目标、前置知识、FAQ
2. **脚本执行**：下载图片、美化格式

## Gemini CLI 处理流程

当用户触发命令时，Ggemini CLI 会：

1. **读取并分析**目标 markdown 文档
2. **智能生成**：
   - 学习目标（4-6个，基于文档内容）
   - 前置知识（相关技术栈）
   - FAQ（如果是教程类型）
3. **插入内容**到文档开头
4. **执行脚本**下载图片和美化格式

## 功能说明

1. **创建 img 文件夹**：在 markdown 文件同目录下创建 `img` 文件夹
2. **下载图片**：提取并下载所有图片到 `img` 文件夹（使用 MD5 哈希命名）
3. **更新引用**：将图片引用更新为本地路径 `./img/filename.jpg`
4. **美化格式**：标题空行、列表规范化、删除多余空行等
5. **AI 内容增强**：智能生成学习目标、前置知识、FAQ（无需配置）

## 脚本说明

Skills 自动执行以下脚本：

```bash
# 1. 美化文档（下载图片、格式化）
python3 ${SKILL_ROOT}/scripts/organize_markdown.py <文件路径> [base_url]

# 2. 增强内容（添加学习目标、前置知识等）
python3 ${SKILL_ROOT}/scripts/enhance_content.py --enhance <文件路径>
```

## 依赖

```bash
pip install requests
```

## 手动运行脚本

```bash
# 脚本位置
ls -la scripts/

# 方式1：依次运行两个脚本
python3 ${SKILL_ROOT}/scripts/organize_markdown.py <文件路径> [base_url]
python3 ${SKILL_ROOT}/scripts/enhance_content.py --enhance <文件路径>

# 方式2：仅运行美化脚本
python3 ${SKILL_ROOT}/scripts/organize_markdown.py <文件路径> [base_url]

# 方式3：仅运行增强脚本
python3 ${SKILL_ROOT}/scripts/enhance_content.py --enhance <文件路径>
```

## 注意事项

- 图片 URL 必须可访问
- 相对路径图片需要提供 base_url 参数
- 已下载的图片不会重复下载
