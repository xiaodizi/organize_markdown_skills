---
argument-hint: <输入markdown文件> [输出HTML文件] [--no-emoji]
description: 将 Markdown 文档转换为微信公众号风格的 HTML，自带一键复制按钮，复制后直接粘贴到公众号编辑器发布
---

# /wechat-format

将 Markdown 文档转换为微信公众号风格的 HTML，自动添加章节 emoji、应用微信排版样式，生成的 HTML 自带一键复制按钮，点击复制后直接粘贴到微信公众号编辑器即可发布。

## 使用方式

### 基本使用
```
/wechat-format <输入markdown文件>
```

### 指定输出文件路径
```
/wechat-format <输入markdown文件> <输出HTML文件>
```

### 不自动添加emoji
```
/wechat-format <输入markdown文件> --no-emoji
```

**示例**：
```
/wechat-format my-article.md
/wechat-format my-article.md my-article-wechat.html
/wechat-format my-article.md --no-emoji
```

## Claude 执行流程

当你执行此命令时，按以下步骤操作：

### 步骤 1：解析参数

- 获取输入 markdown 文件路径
- 如果提供了输出路径则使用，否则自动生成 `{input}_wechat.html`
- 检查 `--no-emoji` 选项

### 步骤 2：运行转换脚本

执行脚本将 Markdown 转换为微信公众号 HTML：

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/wechat-format/scripts/markdown_to_wechat.py <输入markdown文件> [输出HTML文件] [--no-emoji]
```

### 步骤 3：完成提示

脚本执行完成后，告诉用户：
1. 输出 HTML 文件路径
2. 使用方法：在浏览器打开 → 点击右上角"📋 一键复制" → 粘贴到微信公众号编辑器

## 功能特点

- 🎨 自动为章节标题添加 emoji 图标（可关闭）
- 🌐 输出完整 HTML 自带微信公众号阅读样式
- 样式参考优质公众号文章排版，舒适行高、清晰层次
- 📋 页面自带一键复制按钮，点击即复制全部内容
- ✅ 复制后直接粘贴到微信公众号编辑器，样式完美保留

## 依赖

- Python 3.6+
- 需要安装：`pip install markdown`
