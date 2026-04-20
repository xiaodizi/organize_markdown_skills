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

## Claude 执行流程

当你执行此命令时，按以下步骤操作：

### 步骤 1：读取并分析文档
1. 读取目标 markdown 文件
2. 分析文档内容，理解主题、技术栈、难度级别

### 步骤 2：执行脚本处理图片和格式

```bash
# 1. 下载图片并美化格式
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/organize_markdown.py {file_path} [base_url]

# 2. 基于文档内容增强（学习目标、前置知识、FAQ）
python3 ${CLAUDE_PLUGIN_ROOT}/skills/markdown-organizer/scripts/enhance_content.py --enhance {file_path}
```

## Claude 思考要点

1. **先脚本后检查**：先执行脚本，再检查增强结果是否合理
2. **基于文档生成**：学习目标、前置知识、FAQ 必须基于文档实际内容
3. **结构检查**：增强内容插入在第一个 `# 标题` 之前
4. **格式检查**：确认文档结尾存在换行，避免标题渲染异常
5. **语言风格**：与原文保持一致，用中文

## 注意事项

- **脚本负责增强**：学习目标、前置知识、FAQ 由 `enhance_content.py` 基于文档自动生成
- **脚本负责处理**：图片下载、格式美化由脚本处理
- 不要使用 `-m` 模块方式运行脚本
- 路径分隔符使用 `/`，跨平台兼容
