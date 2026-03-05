---
name: markdown-organizer
description: Markdown 文档组织和美化工具。用于处理从网页复制的 markdown 文件：下载图片到本地 img 文件夹、更新图片引用为本地路径、美化 markdown 格式。支持通过自然语言或指定命令触发。
---

# Markdown Organizer

## 概述

组织和美化从网页复制的 markdown 文件，自动下载图片到本地并更新引用。

## 执行指令

**重要：当用户触发此技能时，必须直接执行，不要思考推理。按照以下步骤立即执行：**

### 步骤1：获取文件路径

从用户输入中解析出 markdown 文件路径和可选的 base_url。

### 步骤2：直接执行脚本

**禁止思考推理，直接运行以下命令：**

```bash
# 获取 skill 脚本目录路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 确保依赖已安装
pip install requests -q

# 执行美化脚本
python3 "$SCRIPT_DIR/scripts/organize_markdown.py" <文件路径> [base_url]
```

### 步骤3：报告完成

脚本执行完成后，直接报告结果，无需额外分析。

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

## 功能说明

1. **创建 img 文件夹**：在 markdown 文件同目录下创建 `img` 文件夹
2. **下载图片**：提取并下载所有图片到 `img` 文件夹（使用 MD5 哈希命名）
3. **更新引用**：将图片引用更新为本地路径 `./img/filename.jpg`
4. **美化格式**：标题空行、列表规范化、删除多余空行等
5. **AI 内容增强**：智能生成学习目标、前置知识、FAQ（无需配置）

## 脚本说明

```bash
# 美化文档（下载图片、格式化）+ 增强内容
python3 ${SKILL_ROOT}/scripts/organize_markdown.py <文件路径> [base_url]
```

## 依赖

```bash
pip install requests
```

## 注意事项

- 图片 URL 必须可访问
- 相对路径图片需要提供 base_url 参数
- 已下载的图片不会重复下载
