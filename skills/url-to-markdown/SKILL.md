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

此技能通过 Commands 调用脚本执行：

1. **脚本执行**：获取网页内容、转换为 Markdown、下载图片、美化格式
2. **Claude 处理**：按步骤生成摘要、学习目标、前置知识、FAQ，插入到文档中

## Claude 处理流程

当用户触发命令时，Claude 会按以下步骤执行：

### 第一步：调用脚本转换 URL 为 Markdown

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/url-to-markdown/scripts/url_to_markdown.py <URL> [输出文件路径]
```

### 第二步：分析文档内容

读取转换后的文档，提取：
- 主标题和章节标题
- 首个标题后的核心内容
- 文档的整体主题和难度

### 第三步：生成增强内容

基于文档内容生成五个板块：

**摘要** - 1-3 句话概括文档主要内容

**学习目标** - 3-5 个具体的学习目标

**前置知识** - 3-5 项必需的基础知识

**知识图谱** - Mermaid mindmap 或 flowchart 展现核心概念

**常见问题（FAQ）** - 3-5 个读者可能会有的问题

### 第四步：插入到文档

1. **确定插入位置**：
   - 如果文档有 YAML frontmatter（`---...---`），在 frontmatter 之后
   - 如果没有 frontmatter，在文档最顶部
2. **按顺序插入**五个板块：`## 摘要`、`## 学习目标`、`## 前置知识`、`## 知识图谱`、`## 常见问题`
3. **保持间距**：各板块之间各空一行

### 第五步：检查和保存

验证格式无误、文件末尾有换行，然后保存。

## 功能说明

1. **网页获取**：从 URL 获取网页内容
2. **Markdown 转换**：将 HTML 转换为清晰的 Markdown 格式
3. **创建 img 文件夹**：在 Markdown 文件同目录下创建 `img` 文件夹
4. **下载图片**：提取并下载所有图片到 `img` 文件夹（使用 MD5 哈希命名）
5. **更新引用**：将图片引用更新为本地路径 `./img/filename.jpg`
6. **美化格式**：标题空行、列表规范化、删除多余空行等
7. **内容增强**：基于文档内容自动生成：
   - 摘要、学习目标、前置知识
   - 知识图谱（Mermaid 图）展现核心概念关系
   - FAQ：常见问题和解答

## 脚本说明

Commands 自动执行以下脚本：

```bash
# 1. 获取网页并转换为 Markdown
python3 ${CLAUDE_PLUGIN_ROOT}/skills/url-to-markdown/scripts/url_to_markdown.py <URL> [输出文件路径]

# 2. Claude 按步骤生成增强内容（摘要、学习目标、前置知识、知识图谱、FAQ）
# 并插入到文档顶部

# 3. Claude 检查和保存
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
