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

```bash
# 1. 美化文档（下载图片、格式化）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py <文件路径> [base_url]

# 2. Claude 按步骤执行增强
# - 分析文档内容
# - 生成摘要、学习目标、前置知识、FAQ
# - 插入到文档中
```

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

此技能通过 Commands 调用脚本处理：

1. **脚本处理**：下载图片、美化格式
2. **Claude 处理**：按步骤生成摘要、学习目标、前置知识、FAQ，插入到文档中

## Claude 处理流程

当用户触发命令时，Claude 会按以下步骤执行：

### 第一步：分析文档内容

读取原始文档，提取：
- 主标题和章节标题
- 首个标题后的核心内容
- 文档的整体主题和难度

### 第二步：生成增强内容

基于文档内容生成以下五个板块：

**摘要**
- 1-3 句话概括文档主要内容
- 包含核心概念和适用场景

**学习目标**
- 3-5 个具体的学习目标
- 格式：`- 能够...` 或 `- 理解...`

**前置知识**
- 3-5 项必需的基础知识
- 格式：`- **概念名称**：简短说明`

**知识图谱**
- 生成 Mermaid mindmap 或 flowchart
- 展现文档的核心概念和层级关系
- 格式：```` ```mermaid ... ``` ````

**常见问题（FAQ）**
- 3-5 个读者可能会有的问题
- 格式：`### 问题？\n回答。`

### 第三步：插入到文档

1. **确定插入位置**：
   - 如果文档有 YAML frontmatter，在 frontmatter 之后
   - 如果没有 frontmatter，在文档最顶部
2. **按顺序插入**五个板块：`## 摘要`、`## 学习目标`、`## 前置知识`、`## 知识图谱`、`## 常见问题`
3. **保持间距**：各板块之间各空一行

### 第四步：执行脚本处理图片和格式

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py {file_path} [base_url]
```

这一步自动完成：下载图片、更新图片引用、美化格式。

### 第五步：检查和保存

验证：
- ✓ 所有增强内容基于文档实际内容
- ✓ 没有重复的摘要或概述
- ✓ Markdown 格式正确
- ✓ 文件末尾有换行符

## 关键要点

**内容质量**：每句话都要有意义，基于文档实际内容生成，不要虚构信息。

**位置正确**：增强内容必须在文档顶部（frontmatter 下方），处理图片和格式在插入增强内容之后。

**语言一致性**：与原文保持一致的语言和风格（中文）。

**不修改原文**：只在指定位置添加新内容。

## 功能说明

1. **创建 img 文件夹**：在 markdown 文件同目录下创建 `img` 文件夹
2. **下载图片**：提取并下载所有图片到 `img` 文件夹（使用 MD5 哈希命名）
3. **更新引用**：将图片引用更新为本地路径 `./img/filename.jpg`
4. **美化格式**：标题空行、列表规范化、删除多余空行等
5. **内容增强**：基于文档内容自动生成：
   - 摘要：概括文档主要内容
   - 学习目标：具体的学习成果
   - 前置知识：必需的基础知识
   - 知识图谱：Mermaid 图展现核心概念关系
   - FAQ：常见问题和解答

## 脚本说明

Commands 自动执行以下脚本：

```bash
# Claude 按步骤生成增强内容（摘要、学习目标、前置知识、知识图谱、FAQ）
# 并插入到文档顶部

# 然后执行脚本处理图片和美化格式
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py <文件路径> [base_url]

# 最后 Claude 检查和保存
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
