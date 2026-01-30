---
name: markdown-organizer
description: Markdown 文档组织和美化工具。用于处理从网页复制的 markdown 文件：下载图片到本地 img 文件夹、更新图片引用为本地路径、美化 markdown 格式。支持通过 `/markdown-organizer @文件路径` 命令触发。
---

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

此技能通过 Commands 执行脚本。

**执行流程**：
1. 用户触发 `/markdown-organizer @文件路径`
2. 运行 `organize_markdown.py` 下载图片并美化格式
3. AI Agent 继续进行内容增强（学习目标、前置知识、FAQ 等）

## 功能说明

1. **创建 img 文件夹**：在 markdown 文件同目录下创建 `img` 文件夹
2. **下载图片**：提取并下载所有图片到 `img` 文件夹（使用 MD5 哈希命名）
3. **更新引用**：将图片引用更新为本地路径 `./img/filename.jpg`
4. **美化格式**：标题空行、列表规范化、删除多余空行等
5. **内容增强**：AI Agent 读取美化后的文档，添加学习目标、前置知识、FAQ 等

## 脚本说明

### organize_markdown.py
自动下载图片和美化格式，由 Commands 自动调用。

### enhance_content.py
内容增强辅助工具，供 AI Agent 手动调用：

```bash
# 分析文档结构
python3 enhance_content.py --analyze <文件路径>

# 生成增强建议
python3 enhance_content.py --suggest <文件路径>

# 自动增强内容（添加缺失部分）
python3 enhance_content.py --enhance <文件路径>
```

**功能**：
- 分析文档结构，识别标题层级、代码块、技术术语
- 检测缺失的学习目标、前置知识、FAQ 部分
- 自动添加缺失的内容章节

## 依赖

```bash
pip install requests
```

## 手动运行脚本

```bash
# 查找脚本位置
ls -la ~/.claude/plugins/cache/markdown-organizer/organize_markdown/1.0.0/scripts/

# 运行 organize_markdown.py
python3 .../scripts/organize_markdown.py <文件路径> [base_url]

# 运行 enhance_content.py
python3 .../scripts/enhance_content.py --enhance <文件路径>
```
