---
argument-hint: <URL> [输出文件路径]
description: 将网页 URL 转换为 Markdown 文档并保存到本地，自动下载图片、美化格式、添加学习目标等内容增强
---

# URL to Markdown

将网页 URL 转换为清晰的 Markdown 文档，自动下载图片到本地并更新引用，同时添加学习目标、前置知识等内容增强。

## 使用方式

### 基本使用
```
/url-to-markdown <URL>
```

### 指定输出文件路径
```
/url-to-markdown <URL> <输出文件路径>
```

**示例**：
```
/url-to-markdown https://example.com/post/123
/url-to-markdown https://example.com/post/123 ./docs/article.md
```

## Claude 执行流程

当你执行此命令时，按以下步骤操作：

### 步骤 1：调用脚本获取网页并转换为 Markdown

首先执行脚本将 URL 转换为 Markdown 文件：

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/url-to-markdown/scripts/url_to_markdown.py <URL> [输出文件路径]
```

脚本执行完成后，会显示输出文件的路径。

### 步骤 2：读取并分析生成的文档

1. 读取生成的 Markdown 文件
2. 分析文档内容，理解主题、技术栈、难度级别

### 步骤 3：执行内容增强脚本

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/enhance_content.py --enhance <输出文件路径>
```

## Claude 思考要点

1. **先转换再增强**：先将 URL 转为 Markdown，再执行增强脚本
2. **基于文档生成**：学习目标、前置知识、FAQ 必须基于生成文档的真实内容
3. **结构检查**：增强内容插入在第一个 `# 标题` 之前
4. **格式检查**：确认文档结尾存在换行，避免标题渲染异常
5. **语言风格**：与原文保持一致，用中文

## 注意事项

- **脚本负责增强**：学习目标、前置知识、FAQ 由 `enhance_content.py` 基于文档自动生成
- **脚本负责执行**：网页获取、Markdown 转换、图片下载、格式美化由脚本处理
- **依赖**：需要安装 `pip install requests beautifulsoup4 html2text`
- 不要使用 `-m` 模块方式运行脚本
- 路径分隔符使用 `/`，跨平台兼容
