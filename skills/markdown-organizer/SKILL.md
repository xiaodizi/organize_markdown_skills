---
name: markdown-organizer
description: Markdown 文档组织和美化工具。用于处理从网页复制的 markdown 文件：下载图片到本地 img 文件夹、更新图片引用为本地路径、美化 markdown 格式。支持通过 `/markdown-organizer @文件路径` 命令触发。
---

## 学习目标

完成本教程后，您将能够：

- 理解 Markdown 的核心概念和工作原理
- 掌握 Organizer 的使用方法和使用场景
- 理解文档中涉及的关键术语和技术概念
- 能够按照步骤独立完成实际操作
- 掌握常见问题的排查和解决方法
- 能够将所学知识应用到实际项目中

## 前置知识

本文档涉及以下技术栈和概念，建议提前了解：

- **Python 基础**：了解语法、虚拟环境与 `pip` 常见操作。
- **TypeScript 基础**：了解类型系统、接口与泛型的基本用法。
- **命令行基础**：能在终端完成目录切换、文件操作与命令执行。
- **Markdown 语法**：熟悉标题、列表、代码块与链接等常见语法。

如遇到不熟悉的概念，建议先补充相关基础知识再继续学习。

## 常见问题

### 这篇文档建议按什么顺序学习？
建议按以下顺序阅读并实践：Markdown Organizer -> 概述 -> 使用方式。

### 开始实操前需要准备什么？
建议先准备这些基础：Markdown 语法、Python 基础、TypeScript 基础、命令行基础。

### 实操过程中遇到问题怎么排查？
本文包含约 12 个操作步骤，建议逐步核对输入参数、环境版本和命令执行结果，优先定位首个报错点。

### 学完后如何验证自己掌握了《Markdown Organizer》？
可以尝试脱离文档，独立完成一个最小可运行示例，并正确使用这些关键点：
4. **美化格式**：标题空行、列表规范化、删除多余空行等
5. **AI 内容增强**：、 基于文档内容自动生成学习目标、前置知识、FAQ（无需配置）

## 脚本说明

Commands 自动执行以下脚本：

、bash

# 1. 美化文档（下载图片、格式化）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py <文件路径> [base_url]

# 2. 增强内容（添加学习目标、前置知识等）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/enhance_content.py --enhance <文件路径>
。

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

此技能通过 Commands 调用脚本执行：

1. **脚本处理**：下载图片、美化格式
2. **脚本增强**：基于文档内容自动生成学习目标、前置知识、FAQ

## Claude 处理流程

当用户触发命令时，Claude 会：

1. **执行脚本**下载图片和美化格式
2. **执行增强脚本**基于文档内容生成学习目标、前置知识、FAQ
3. **检查结果**：确认增强内容在第一个标题前，且文档末尾有换行

## 功能说明

1. **创建 img 文件夹**：在 markdown 文件同目录下创建 `img` 文件夹
2. **下载图片**：提取并下载所有图片到 `img` 文件夹（使用 MD5 哈希命名）
3. **更新引用**：将图片引用更新为本地路径 `./img/filename.jpg`
4. **美化格式**：标题空行、列表规范化、删除多余空行等
5. **AI 内容增强**：`enhance_content.py` 基于文档内容自动生成学习目标、前置知识、FAQ（无需配置）

## 脚本说明

Commands 自动执行以下脚本：

```bash

# 1. 美化文档（下载图片、格式化）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py <文件路径> [base_url]

# 2. 增强内容（添加学习目标、前置知识等）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/enhance_content.py --enhance <文件路径>
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
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py <文件路径> [base_url]
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/enhance_content.py --enhance <文件路径>

# 方式2：仅运行美化脚本
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py <文件路径> [base_url]

# 方式3：仅运行增强脚本
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/enhance_content.py --enhance <文件路径>
```
