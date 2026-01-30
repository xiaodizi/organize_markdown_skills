---
argument-hint: [@文件路径] [base_url]
description: 组织和美化 markdown 文档，下载图片到本地 img 文件夹
---

# Markdown Organizer

处理从网页复制的 markdown 文件，自动下载图片到本地并更新引用。

## 使用方式

### 基本使用
```
/markdown-organizer @文件路径
```

### 指定源 URL（处理相对路径图片）
```
/markdown-organizer @文件路径 https://example.com/post/123
```

## 执行步骤

1. 解析用户输入，获取 markdown 文件路径（@后跟着的文件路径）和可选的 base_url
2. 执行脚本：`python3 {skill_dir}/scripts/organize_markdown.py {file_path} [base_url]`

其中 `{skill_dir}` 在运行时会被替换为插件安装路径：
- macOS: `~/.claude/plugins/cache/markdown-organizer/organize_markdown/1.0.0/`
- Windows: `%USERPROFILE%\.claude\plugins\cache\markdown-organizer\organize_markdown\1.0.0\`

**重要：**
- 使用 `python3` 命令直接运行脚本，**不要**使用 `-m` 模块方式
- 脚本是独立脚本，不是 Python 模块
- 路径分隔符使用 `/`，跨平台兼容
