---
name: markdown-organizer
description: Markdown 文档组织和美化工具。用于处理从网页复制的 markdown 文件：下载图片到本地 img 文件夹、更新图片引用为本地路径、美化 markdown 格式。支持通过 `/markdown-organizer @文件路径` 命令触发。
---


## 自动化执行流程

当用户通过 `/markdown-organizer @文件路径` 命令触发此技能时，Agent 必须严格遵循以下步骤，无需用户中途确认或干预：

### 第一步：读取并分析文件
1. 读取用户指定的 Markdown 文件内容。
2. **（可选）处理 Web Clipper 元数据**：如果文件包含来自网页剪藏的元数据（如 `title`, `source`），则将其合并到 YAML frontmatter 中，并使用 `title` 字段在 frontmatter 后创建一级标题（`# 标题`）。

### 第二步：生成增强内容
1. 基于文件内容，在内部生成以下两个部分：
   - **摘要**：对全文进行概括。
   - **知识图谱**：使用 Mermaid 的 `mindmap` 格式展示核心概念。

### 第三步：将增强内容写入文件
1. 将上一步生成的 **摘要** 和 **知识图谱** 作为一个整体，插入到文件的 YAML frontmatter 结束标记 (`---`) 之后，正文内容之前。
2. 确保插入的内容与原文之间有适当的空行分隔。


### 第四步：Mermaid 语法检测与自动修复（可选强烈推荐）
1. 在插入知识图谱后，自动执行以下流程，确保 Mermaid 代码块无语法错误：
   1.1 提取所有 mermaid 代码块：
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/extract_mermaid_blocks.py <文件路径>
   ```
   1.2 用 Mermaid CLI 检查每个 .mmd 文件语法：
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/check_mermaid_syntax.py mermaid_block_X.mmd
   ```
   1.3 如检测到语法错误，自动修复：
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/fix_mermaid_nodes.py mermaid_block_X.mmd
   # 修复后再次检测，直到无错
   ```
2. 检查全部通过后，继续执行格式化与图片处理脚本：
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py <文件路径> [base_url]
   ```

### 第五步：完成并报告
1. 脚本执行成功后，向用户显示最终的完成报告。报告应简要说明已添加的内容（摘要、知识图谱）和处理的图片数量（如果有）。
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
5. **AI 内容增强**：、 基于文档内容自动生成摘要、知识图谱等增强内容，并正确插入到文档中。

## 脚本说明

Commands 自动执行以下脚本：

```bash
# 1. 美化文档（下载图片、格式化）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py <文件路径> [base_url]
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

## AI 处理流程

当用户触发命令时，AI Agent（如 Claude、Gemini、GPT-4 等）应按以下步骤执行：

### 第零步：处理 Web Clipper 元数据（可选）

如果文件顶部包含 Web Clipper 格式的元数据（title, source, author, published 等）：

1. **合并 frontmatter**：
   - 识别 YAML frontmatter 中的 Web Clipper 属性（`title`、`source`、`author`、`published` 等）
   - 将这些属性与文档现有的 frontmatter 合并
   - 如果现有 frontmatter 已有相同字段，以现有内容为准
   - 保留 `title` 字段在 frontmatter 中

2. **生成文档一级标题**：
   - 在 frontmatter 的结束标记（`---`）之后，插入一个空行
   - 然后插入 `# {title字段内容}` 作为文档的一级标题
   - 确保标题和原文内容之间有一个空行
   - 例如：如果 title 是 "AI Knowledge Layer"，则插入 `# AI Knowledge Layer`

3. **清理和验证**：
   - 删除已处理的 Web Clipper 临时元数据部分（如果有）
   - 检查 frontmatter 格式正确（YAML 语法无误）
   - 确保生成的文档结构清晰

**文件结构示例**：
```yaml
---
title: AI Knowledge Layer
source: https://example.com
author: Author Name
---

# AI Knowledge Layer

原文内容...
```

**如果文档没有 Web Clipper 元数据或没有 `title` 字段，直接跳过此步骤。**

### 第一步：分析文档内容

读取原始文档，提取：
- 主标题和章节标题
- 首个标题后的核心内容
- 文档的整体主题和难度

### 第二步：生成增强内容

基于文档内容生成以下两个板块：

**摘要**
- 1-3 句话概括文档主要内容
- 包含核心概念和适用场景

**知识图谱**
- 生成 Mermaid mindmap 或 flowchart
- 展现文档的核心概念和层级关系
- 格式：```` ```mermaid ... ``` ```
- **Mermaid 语法规范**（Obsidian 兼容）：
   - **推荐**：mindmap 格式（最安全）
   - **可用的节点形状**：
      - 矩形：`[文本]`
      - 圆角矩形：`(文本)`
      - 菱形：`{文本}`
   - **禁止**：`[/text]`、`[\text]`、`([text])`、`{{text}}`、`xxx()`、`xxx[]`、`xxx{}`、`xxx<>`、`xxx/`、`xxx\` 等复杂或特殊符号、函数、括号写法
   - 节点内容**只能用纯文本**，不能有括号、函数、特殊符号（如 cognify()、func{}、data[] 等）
   - 避免在节点文本中使用特殊字符（保持简洁）
- 包含 3-5 个主要概念的层级关系

### 第三步：更新文件

现在将第二步生成的四个板块直接写入文件：

1. **确定插入位置**：
   - 如果文档有 YAML frontmatter，在 frontmatter 之后
   - 如果没有 frontmatter，在文档最顶部

2. **构建完整内容**：
    - 根据第二步的内容，拼接以下两个板块：
       1. `## 摘要` + 摘要内容
       2. `## 知识图谱` + Mermaid 代码块
    - 确保块之间各空一行

3. **保存文件**：
   - 在确定的插入位置插入这些内容
   - 确保最后一个块和原文内容之间空一行
   - 确保文件末尾有换行符
   - **立即将修改保存到文件**

### 第四步：执行脚本处理图片和格式

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py {file_path} [base_url]
```

这一步自动完成：下载图片、更新图片引用、美化格式。

### 第五步：完成并报告

自动检查和确认（不需要用户确认）：

1. **自动验证**：
   - ✓ 验证所有增强内容都基于文档实际内容
   - ✓ 确认没有重复的摘要（如文档已有 "## 摘要" 或 "## 概述"，应已跳过）
   - ✓ 检查 Markdown 格式正确无误
   - ✓ 确保文件末尾有换行符

2. **生成完成报告**（直接显示，无需询问）：
   - 📝 列出已插入的两个内容块
   - 🖼️ 报告已下载的图片数量和更新情况
   - ✅ 确认文件已保存的路径
   - 📊 简要说明增强内容的质量检查结果

**重要**：不要询问用户是否需要"预览"或"diff"，直接完成并显示简明报告即可。

## 关键要点

**内容质量**：每句话都要有意义，基于文档实际内容生成，不要虚构信息。

**Mermaid 图谱节点内容规范**：所有节点内容必须为纯文本，禁止括号、函数、特殊符号等写法（如 cognify()、func{}、data[] 等），否则会导致解析错误。

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
   - 知识图谱：Mermaid 图展现核心概念关系

## 脚本说明

Commands 自动执行以下脚本：

```bash
# AI Agent 按步骤生成增强内容（摘要、知识图谱）
# 并插入到文档顶部

# 然后执行脚本处理图片和美化格式
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py <文件路径> [base_url]

# 最后 AI Agent 检查和保存
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

# 方式3：makrdown 格式化增强工具
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/enhance_content.py --enhance <文件路径>
```
