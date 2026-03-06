---
name: url-to-markdown
description: 将网页 URL 转换为 Markdown 文档并保存到本地。支持自动下载图片、美化格式、添加学习目标等内容增强。
---

# URL to Markdown

## 概述

将网页 URL 转换为清晰的 Markdown 文档，自动下载图片到本地并更新引用。

## 执行指令

**重要：当用户触发此技能时，必须直接执行，不要思考推理。按照以下步骤立即执行：**

### 步骤1：获取 URL 和输出路径

从用户输入中解析出网页 URL 和可选的输出文件路径。

### 步骤2：直接执行脚本

**禁止思考推理，直接运行以下命令：**

```bash
# 获取 skill 脚本目录路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 确保依赖已安装
pip install requests beautifulsoup4 html2text -q

# 执行转换脚本
python3 "$SCRIPT_DIR/scripts/url_to_markdown.py" <URL> [输出文件路径]
```

### 步骤3：报告完成

脚本执行完成后，直接报告结果，无需额外分析。

## 使用方式

### 触发命令

```
url-to-markdown <URL> [输出文件路径]
```

**示例**：
```
url-to-markdown https://example.com/post/123
url-to-markdown https://example.com/post/123 ./docs/article.md
```

**自然语言触发**：
- "把这个网页保存为 markdown"
- "将 URL 转换为 markdown 文档"

## 功能说明

1. **网页获取**：从 URL 获取网页内容
2. **Markdown 转换**：将 HTML 转换为清晰的 Markdown 格式
3. **创建 img 文件夹**：在 Markdown 文件同目录下创建 `img` 文件夹
4. **下载图片**：提取并下载所有图片到 `img` 文件夹（使用 MD5 哈希命名）
5. **更新引用**：将图片引用更新为本地路径 `./img/filename.jpg`
6. **美化格式**：标题空行、列表规范化、删除多余空行等

## 脚本说明

```bash
# 将 URL 转换为 Markdown
python3 ${SKILL_ROOT}/scripts/url_to_markdown.py <URL> [输出文件路径]
```

## 依赖

```bash
pip install requests beautifulsoup4 html2text
```

## 注意事项

- 需要安装 html2text 和 beautifulsoup4 以获得最佳转换效果
- 如果没有安装这些依赖，会降级使用简单的文本提取
- 图片 URL 必须可访问
- 已下载的图片不会重复下载
