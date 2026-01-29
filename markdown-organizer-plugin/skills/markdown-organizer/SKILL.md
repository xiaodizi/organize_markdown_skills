---
name: markdown-organizer
description: Markdown 文档组织和美化工具。用于处理从网页复制的 markdown 文件：下载图片到本地 img 文件夹、更新图片引用为本地路径、美化 markdown 格式。支持通过 `/markdown-organizer @文件路径` 命令触发，或当用户说 "@文件路径" 或 "帮我美化文档" 或提到处理包含图片的 markdown 文件时使用此技能。
---

# Markdown Organizer

## 概述

组织和美化从网页复制的 markdown 文件，自动下载图片到本地并更新引用。

## 工作流程

### 1. 识别触发条件

当用户满足以下任一条件时触发此技能：
- 使用 `@` 符号指定本地 markdown 文件路径
- 说"帮我美化文档"或类似请求
- 提到处理包含图片的 markdown 文件

### 2. 执行脚本

运行 `{plugin_dir}/organize_markdown.py` 处理文件，使用绝对路径确保正确执行：

```bash
python3 {plugin_dir}/organize_markdown.py /path/to/file.md [base_url]
```

其中 `{skill_dir}` 是技能目录的绝对路径（SKILL.md 所在目录）。

其中 `{plugin_dir}` 是插件目录的绝对路径。

**参数说明：**
- `file.md`: markdown 文件路径（必需）
- `base_url`: 原文章页面的 URL（可选，用于处理相对路径的图片）

### 3. 脚本功能

脚本会自动执行以下操作：

1. **创建 img 文件夹**：在 markdown 文件同目录下创建 `img` 文件夹（如果不存在）

2. **提取图片 URL**：扫描 markdown 文件，提取所有图片引用 `![alt](url)`

3. **下载图片**：
   - 将图片下载到 `img` 文件夹
   - 使用 URL 的 MD5 哈希值作为文件名（避免文件名过长或包含非法字符）
   - 保留原始图片扩展名
   - 如果文件已存在则跳过下载

4. **更新图片引用**：将 markdown 中的图片引用更新为本地路径 `![alt](./img/filename.jpg)`

5. **美化 markdown 格式**：
   - 标题前后添加空行
   - 统一列表标记为 `- `
   - 规范化代码块
   - 删除多余空行
   - 去除行尾空格

## 脚本位置

```
organize_markdown.py
```

## 使用示例

### 示例 1：基本使用

用户说：
```
@/Users/user/articles/python-tutorial.md 帮我美化文档
```

执行：
```bash
python3 organize_markdown.py /Users/user/articles/python-tutorial.md
```

### 示例 2：指定源 URL

用户说：
```
@article.md 美化这个文档，原页面是 https://example.com/post/123
```

执行：
```bash
python3 organize_markdown.py article.md https://example.com/post/123
```

## 依赖

脚本需要以下 Python 包：
- `requests`: 下载图片
