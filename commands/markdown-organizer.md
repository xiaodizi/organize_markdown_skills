---
argument-hint: [@文件路径] [base_url]
description: 组织和美化 markdown 文档，自动下载图片到本地 img 文件夹，并添加学习目标、前置知识等内容增强
---

# Markdown Organizer

处理从网页复制的 markdown 文件，自动下载图片到本地并更新引用，并添加学习目标、前置知识等内容增强。

## 使用方式

### 基本使用
```
/markdown-organizer @文件路径
```

### 指定源 URL（处理相对路径图片）
```
/markdown-organizer @文件路径 https://example.com/post/123
```

## 默认行为

- 📁 **图片下载**：自动下载所有网络图片到本地 `img/` 文件夹
- 💾 **文件保存**：自动保存并覆盖原文件（包括 frontmatter、增强内容、图片引用）
- ✨ **无需确认**：完整的处理流程自动执行，无需用户中途确认

## Claude 执行流程

当你执行此命令时，Claude **完全自动执行**以下所有步骤，**无需任何用户确认**：

### 步骤 1：读取并分析文档

1. 读取原始 markdown 文件
2. 提取：
   - 标题（`# ` 开头）- 作为文档的一级标题
   - 二级标题列表（`## ` 开头）- 作为主要章节
   - 首个标题后的前 3-5 个段落
   - 文档的整体主题和核心内容

### 步骤 2：基于文档内容生成增强内容

基于文档的实际内容，生成以下内容块（每块都要相关且高质量）：

**▌ 摘要**
- 简洁概括：1-3 句话说明这篇文档主要讲什么
- 包含核心概念和适用场景

**▌ 知识图谱**
- 基于文档内容生成 Mermaid mindmap 或简单 flowchart
- 展现文档的核心概念及其关系
- **Mermaid 语法规范**（确保 Obsidian 兼容）：
  - 优先使用 `mindmap` 格式（最兼容）
  - 如使用 `graph TD` 或 `flowchart TD`，只使用基础节点形状：
    - `[文本]` - 矩形框
    - `(文本)` - 圆角矩形
    - `{文本}` - 菱形
  - **不要使用**：`[/text]`、`[\text]`、`([text])`、`{{text}}` 等复杂形状
- 格式：```` ```mermaid ... ``` ````
- 包含 3-5 个主要章节和关键概念的层级关系

### 步骤 3：更新文件

现在将步骤 2 生成的五个内容块直接写入文件（如果步骤 0 已处理，插入位置在新添加的一级标题之后）：

1. **确定插入位置**：
   - 如果文档有 YAML frontmatter（`---...---`），插入位置在 frontmatter 之后
   - 如果没有 frontmatter，插入到文档最顶部

2. **构建完整内容**：
   - 根据步骤 2 的内容，拼接以下两个板块：
     1. `## 摘要` + 摘要内容
     2. `## 知识图谱` + Mermaid 代码块
   - 确保块之间各空一行

3. **保存文件**：
   - 在确定的插入位置插入这些内容
   - 确保最后一个块和原文内容之间空一行
   - 确保文件末尾有换行符
   - **立即将修改保存到文件**

### 步骤 4：处理图片、格式和 Web Clipper 元数据

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py {file_path} [base_url]
```

这一步自动完成以下所有操作（必选项）：

**Part A：处理 Web Clipper 元数据**
- 🔍 **合并多个 frontmatter 块**：如果文档包含多个 frontmatter 块（Obsidian 笔记属性 + Web Clipper 元数据），自动将其合并成一个单一的笔记属性块
  - 删除 Web Clipper 的元数据块本身
  - 将所有 Web Clipper 字段（source、author、published、description 等）合并到笔记属性中
  - 对于重复字段（如 tags、title），进行智能去重和合并
- 📌 **生成一级标题**：如果文档缺少一级标题（`# 标题`），自动从 frontmatter 的 `title` 字段生成
  - title 为空或"未命名"时，跳过生成
  - 生成的一级标题位置在所有内容增强块之后

**Part B：处理图片和格式**
- ⬇️ 下载图片到本地 `img/` 文件夹
- 🔗 更新 markdown 中的图片引用为本地路径
- ✨ 美化 markdown 格式（标题、列表、空行等）

**Part C：保存和验证**
- 💾 **回填并保存所有笔记属性到文件**（包括 frontmatter、增强内容、图片引用等）
- ✓ 确保文件末尾有换行符

**处理示例**：

输入（Web Clipper + Obsidian 两个 frontmatter 块）：
```markdown
---
title: 未命名
aliases: []
tags: [知识库/AI]
updated: 2026-04-21T13:26:05
created: 2026-04-21T13:26:05
up: ""
related: []
summary: ""
---
---
title: "AI Knowledge Layer (and why your agents are useless without it)"
source: "https://x.com/example"
author: ["John Doe"]
published: 2026-04-14
tags: [clippings, AI]
description: "A comprehensive guide about how to build AI knowledge systems"
---

[原始文档内容...]
```

输出（合并为一个笔记属性块，删除 Web Clipper 块）：
```markdown
---
title: AI Knowledge Layer (and why your agents are useless without it)
aliases: []
tags:
- 知识库/AI
- clippings
- AI
updated: 2026-04-21 13:26:05
created: 2026-04-21 13:26:05
up: ''
related: []
summary: ''
source: https://x.com/example
author:
- John Doe
published: 2026-04-14
description: A comprehensive guide about how to build AI knowledge systems
---

## 摘要
...

# AI Knowledge Layer (and why your agents are useless without it)

[原始文档内容...]
```

**关键点**：
- ✅ 两个 frontmatter 块合并为一个笔记属性块
- ✅ Web Clipper 元数据块已删除（不再有第二个 `---...---` 块）
- ✅ Obsidian title（"未命名"）被替换为 Web Clipper 的有意义标题
- ✅ tags 去重合并：`[知识库/AI, clippings, AI]`
- ✅ 所有 Web Clipper 字段保留在笔记属性中：source、author、published、description
- ✅ 一级标题（# 标题）自动从 title 字段生成，位置在所有内容增强块之后

### 步骤 5：Claude 验证并报告（自动执行）

脚本执行完成后，Claude 自动进行最终验证和报告（不需要任何用户确认）：

1. **验证脚本执行结果**：
   - ✓ 确认文件已成功保存
   - ✓ 验证 frontmatter 属性已正确合并和保存
   - ✓ 验证一级标题（`# ` 开头）已存在或已自动生成
   - ✓ 确认增强内容都基于文档实际内容
   - ✓ 确认没有重复的摘要（如文档已有 "## 摘要" 或 "## 概述"，应已跳过）
   - ✓ 检查 Markdown 格式正确无误
   - ✓ 确保文件末尾有换行符

2. **生成完成报告**（直接显示，无需询问）：
   - 📝 列出已插入的增强内容块（摘要、学习目标、知识图谱、常见问题）
   - 🖼️ 报告已下载的图片数量和更新情况
   - 📋 报告已合并的 frontmatter 属性（如 tags、categories 等）
   - 📌 报告一级标题情况（已存在 / 新创建 + 标题内容）
   - ✅ 确认文件已保存的路径及最后修改时间

**重要**：不要询问用户是否需要"预览"或"diff"，直接完成并显示简明报告即可。

## 执行要点

1. **完全自动执行**：无需中途确认，所有步骤自动完成（步骤 1-5）
2. **内容质量优先**：每一句都要有意义，基于文档实际内容，不要生成虚假或不相关的信息
3. **语言风格**：与原文保持一致，用中文表述
4. **难度匹配**：学习目标和前置知识要与文档难度相匹配
5. **位置正确**：增强内容必须在文档顶部（frontmatter 下方），其他原文顺序不变
6. **Web Clipper 必选**：frontmatter 合并、一级标题生成、属性保留都是必选项
7. **不要做**：不要修改原文内容，只在指定位置添加新内容
