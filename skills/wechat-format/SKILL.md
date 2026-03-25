---
name: wechat-format
description: 将普通 Markdown 文档格式化为微信公众号风格，自动添加章节 emoji、生成目录、优化段落间距和列表格式，让排版更清晰美观。使用当需要将 markdown 文章导出为微信公众号格式排版时。
---

# WeChat Format 微信公众号排版

## Overview

将普通 Markdown 文档自动格式化为微信公众号风格的清晰排版：
- 自动为章节标题匹配合适的 emoji 图标
- 自动生成 Table of Contents 目录
- 优化段落间距和列表格式
- 增强重点内容可读性
- 保持原有内容不变，只美化格式

## 快速开始

### 输出微信公众号 HTML（推荐，直接复制粘贴使用）

将 markdown 转换为带微信公众号样式的 HTML，可一键复制后直接粘贴到微信公众号编辑器：

```bash
python3 skills/wechat-format/scripts/markdown_to_wechat.py <输入文件.md> [输出文件.html]
```

打开生成的 HTML 文件，点击右上角 **📋 一键复制** 按钮，然后直接粘贴到微信公众号编辑器即可。

### 仅格式化 Markdown

如果你只需要格式化 markdown 格式（保留 emoji 和目录），仍然可以使用：

```bash
python3 skills/wechat-format/scripts/format_wechat.py <输入文件.md> [输出文件.md]
```

### 选项

- `--no-emoji`：不自动添加 emoji 到章节标题
- `--no-toc`：不生成目录（仅 format_wechat.py）

## 功能特性

### 1. 自动章节 Emoji

根据章节标题关键词自动匹配合适的 emoji：

| 关键词 | Emoji |
|--------|-------|
| 概览、概述、简介、介绍 | 🔍 |
| 背景、相关 | 📚 |
| 原理、理论、概念 | 💡 |
| 方法、步骤、流程、实践 | ⚙️ |
| 最佳实践、推荐 | ✨ |
| 示例、案例 | 📝 |
| 问题、故障、错误 | ⚠️ |
| 解决、方案 | ✅ |
| 对比、比较 | ⚖️ |
| 总结、结语 | 🎯 |
| 参考、链接 | 🔗 |
| 安装、部署 | 🚀 |
| 配置、设置 | ⚙️ |
| 使用、用法 | 📖 |
| 特性、功能 | 🌟 |
| 性能、优化 | ⚡ |
| 安全、风险 | 🔒 |
| 测试、验证 | 🧪 |
| 架构、设计 | 🏗️ |
| 实现、开发 | 👨‍💻 |
| 未来、展望 | 🔮 |

没有匹配关键词时按标题层级使用默认 emoji：
- H1: 📌
- H2: ⚡
- H3: 🔸
- H4: ▫️

### 2. 自动生成目录

在标题后自动提取所有章节生成 Table of Contents 目录，方便读者快速导航。

### 3. 段落间距优化

确保：
- 标题后有适当空行
- 段落之间空一行
- 删除多余的连续空行
- 列表前后保持适当间距

### 4. 列表格式优化

优化列表项的间距，让长列表更易读。

## Claude 工作流程

当用户要求"格式化成微信公众号风格"或类似需求时：

1. **确认输入文件**：获取要格式化的 markdown 文件路径
2. **运行格式化脚本**：
   ```bash
   python3 skills/wechat-format/scripts/format_wechat.py <输入文件> [输出文件]
   ```
3. **读取结果**：检查格式化后的输出
4. **完成**：告知用户输出文件路径

## 使用示例

### 示例 1：基本格式化

```bash
python3 skills/wechat-format/scripts/format_wechat.py my_article.md
# 输出: my_article_wechat.md
```

### 示例 2：指定输出路径

```bash
python3 skills/wechat-format/scripts/format_wechat.py input.md output.md
```

### 示例 3：不生成目录

```bash
python3 skills/wechat-format/scripts/format_wechat.py input.md --no-toc
```

## 格式化效果对比

**格式化前：**
```markdown
# AI编程如何告别屎山代码

## 概览

软件开发正在经历一场深刻的范式变革。

## 传统 SDLC

传统瀑布式 / 敏捷 SDLC 流程：需求分析 → 系统设计 → 编码开发 → 测试验证 → 部署上线 → 维护迭代
```

**格式化后：**
```markdown
# 📌 AI编程如何告别屎山代码

## 🔍 概览

软件开发正在经历一场深刻的范式变革。

## ⚡ 传统 SDLC

传统瀑布式 / 敏捷 SDLC 流程：需求分析 → 系统设计 → 编码开发 → 测试验证 → 部署上线 → 维护迭代
```

## 脚本参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `input` | 是 | 输入 markdown 文件路径 |
| `output` | 否 | 输出文件路径，默认 `{input}_wechat.md` |
| `--no-toc` | 否 | 跳过目录生成 |

### 5. 微信风格 HTML 输出

将 markdown 直接转换为带完整 CSS 样式的 HTML，适配微信公众号阅读体验：

- 舒适行高 `1.8`，适合手机阅读
- 清晰标题层级区分
- 代码块美化，左侧蓝色标识条
- 引用块和表格样式优化
- 图片自适应宽度
- 响应式设计，支持手机/桌面

### 6. 一键复制按钮

生成的 HTML 页面右上角自带 **📋 一键复制** 按钮，点击即可复制全部内容，直接粘贴到微信公众号编辑器，样式完美保留。

## 样式特点

生成的 HTML 参考了优质微信公众号文章的排版风格，和你提供的示例文章 `https://mp.weixin.qq.com/s/gIzGWlN-KJIT7uIucojB4A` 风格一致：
- 清晰的章节层级
- 适当的留白和间距
- 重点内容加粗突出
- 舒服的字体大小和行高
- 干净清爽的阅读体验

## Claude 工作流程

当用户要求"格式化成微信公众号风格"或类似需求时：

1. **确认输入文件**：获取要格式化的 markdown 文件路径
2. **生成 HTML**：
   ```bash
   python3 skills/wechat-format/scripts/markdown_to_wechat.py <输入文件.md> [输出文件.html]
   ```
3. **告知用户**：输出 HTML 文件路径，说明打开后点击一键复制，粘贴到公众号编辑器

如果用户只需要 markdown 格式化，使用：
```bash
python3 skills/wechat-format/scripts/format_wechat.py <输入文件> [输出文件]
```

## 使用示例

### HTML 输出（推荐用于微信公众号发布）

```bash
python3 skills/wechat-format/scripts/markdown_to_wechat.py my_article.md
# 输出: my_article_wechat.html
```

打开 HTML 文件 → 点击"📋 一键复制" → 粘贴到微信公众号编辑器 → 完成发布！

### 不添加 emoji

```bash
python3 skills/wechat-format/scripts/markdown_to_wechat.py input.md --no-emoji
```

### 指定输出路径

```bash
python3 skills/wechat-format/scripts/markdown_to_wechat.py input.md output.html
```

## 脚本参数

### markdown_to_wechat.py (HTML 输出)

| 参数 | 必填 | 说明 |
|------|------|------|
| `input` | 是 | 输入 markdown 文件路径 |
| `output` | 否 | 输出 HTML 文件路径，默认 `{input}_wechat.html` |
| `--no-emoji` | 否 | 不自动添加 emoji 到章节标题 |

### format_wechat.py (Markdown 格式化)

| 参数 | 必填 | 说明 |
|------|------|------|
| `input` | 是 | 输入 markdown 文件路径 |
| `output` | 否 | 输出文件路径，默认 `{input}_wechat.md` |
| `--no-toc` | 否 | 跳过目录生成 |

## 依赖

- Python 3.6+
- `markdown` 包（仅 HTML 输出需要）：`pip install markdown`
- `format_wechat.py` 仅使用标准库，无需额外依赖

