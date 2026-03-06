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

### 步骤 3：生成学习目标和前置知识（Claude 智能思考）

根据文档内容，生成以下内容插入到文档开头（第一个 # 标题之前）：

**学习目标**：
- 分析文档主题，提取 4-6 个具体可衡量的学习目标
- 目标应该具体、可执行，例如："能够使用 X 完成 Y"
- 格式：`- 目标描述`

**前置知识**：
- 分析文档涉及的技术栈（Python/API/Git 等）
- 列出阅读本文档需要的前置知识
- 格式：`- **技术栈名称**：描述`

**FAQ**（如果文档是教程类型）：
- 根据文档内容生成 2-3 个常见问题
- 格式：`### 问题\n答案`

### 步骤 4：执行内容增强脚本

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/enhance_content.py --enhance <输出文件路径>
```

## Claude 思考要点

1. **理解文档**：阅读文档内容，判断是教程/概念/参考/故障排查
2. **提取关键词**：识别技术栈、工具、方法
3. **生成目标**：基于文档章节和内容，生成有意义的学习目标
4. **生成前置知识**：识别文档假设读者已具备的知识
5. **插入位置**：在第一个 `# 标题` 之前插入
6. **语言风格**：与原文保持一致，用中文

## 注意事项

- **Claude 负责思考**：学习目标、前置知识、FAQ 由 Claude 智能生成
- **脚本负责执行**：网页获取、Markdown 转换、图片下载、格式美化由脚本处理
- **依赖**：需要安装 `pip install requests beautifulsoup4 html2text`
- 不要使用 `-m` 模块方式运行脚本
- 路径分隔符使用 `/`，跨平台兼容
