# Markdown Organizer

组织和美化从网页复制的 Markdown 文档，自动下载图片到本地并更新引用，利用 Claude 的智能思考生成学习目标和前置知识。

![](./img/f5339aeb70e245d782f288ba17ace4ff.jpg)

## ✨ 功能特性

| 功能 | 描述 |
|------|------|
| 📥 **图片本地化** | 自动下载 Markdown 中的图片到 `img` 文件夹，使用 MD5 哈希命名避免冲突 |
| 🔗 **路径更新** | 将图片引用从网络 URL 自动更新为本地路径 `./img/filename.jpg` |
| 🎨 **格式美化** | 标题空行、列表规范化、删除多余空行，统一格式 |
| 🤖 **AI 内容增强** | Claude 智能生成学习目标、前置知识、FAQ（无需配置） |

## 🚀 快速开始

### 安装

#### Claude Code 插件安装

```bash
# 1. 添加市场源
/plugin marketplace add xiaodizi/organize_markdown_skills

# 2. 安装插件
/plugin install organize_markdown@markdown-organizer
```

#### Gemini CLI 安装

```bash
# 安装 skill（需要指定 skill 路径）
gemini skills install https://github.com/xiaodizi/organize_markdown_skills.git --path .gemini/skills/markdown-organizer
```

> ⚠️ 注意：由于 Claude Code 和 Gemini CLI 使用不同的 skill 格式，skill 文件放在 `.gemini/skills/` 子目录中，因此需要使用 `--path` 参数指定路径。

```bash
# 安装 skill（会自动发现 .gemini/skills 目录）
gemini skills install https://github.com/xiaodizi/organize_markdown_skills.git

# 或者指定具体路径安装
gemini skills install https://github.com/xiaodizi/organize_markdown_skills.git --path .gemini/skills/markdown-organizer
```

##### Gemini CLI 使用

```bash
# 查看已安装的 skills
gemini skills list

# 在 Gemini CLI 会话中启用 skill
/organize-markdown @文件路径

# 或者使用自然语言
# "帮我美化这个 markdown 文档"
```

### 使用

```bash
# 基本用法
/markdown-organizer @/path/to/article.md

# 处理相对路径图片（需要提供原网页 URL）
/markdown-organizer @article.md https://example.com/post/123
```

### 自然语言触发

- `"@文件路径 帮我美化文档"`
- `"处理这个 markdown 文件"`

## 📖 详细说明

### 更新日志

| 版本 | 说明 |
|------|------|
| v1.0.4 | 新增 Gemini CLI 技能支持、直接执行命令 `/organize`、优化文档结构 |
| v1.0.2 | Claude 智能思考生成学习目标和前置知识（无需配置）、自动更新检查 |
| v1.0.1 | 精简目录结构，优化变量加载路径 |
| v1.0.0 | 初始版本发布 |

当您运行命令时，Claude 会：

1. **阅读并分析**目标文档内容
2. **智能生成**：
   - 学习目标（4-6个，基于文档主题和章节）
   - 前置知识（识别相关技术栈）
   - FAQ（如文档是教程类型）
3. **自动插入**内容到文档开头
4. **执行脚本**下载图片和美化格式

所有内容生成由 Claude 智能完成，**无需任何 API 配置**。

### 图片处理

- 支持 `![alt](url)` 和 `![alt](relative/path)` 语法
- 相对路径图片会自动与 `base_url` 组合
- 图片保存为 `img/[md5hash].jpg`
- 已下载的图片不会重复下载

## 📂 项目结构

```
organize_markdown_skills/
├── .claude-plugin/                   # 插件配置（发布时由 GitHub 读取）
│   ├── plugin.json                   # 插件元数据（名称、版本、命令、技能等）
│   └── marketplace.json              # 市场配置（发布到插件市场）
├── .gemini/                          # Gemini CLI 配置
│   └── skills/
│       └── markdown-organizer/       # Gemini CLI Skill
│           ├── SKILL.md              # 技能说明
│           └── scripts/               # Python 脚本
├── commands/                         # 命令快捷方式
│   └── markdown-organizer.md         # /markdown-organizer 命令定义
├── hooks/                            # 插件钩子
│   ├── hooks.json                    # 钩子配置
│   ├── check-deps.sh                 # 依赖检查（会话启动时自动安装 requests）
│   └── check-update.sh               # 更新检查（会话启动时检查新版本）
├── skills/                           # Claude Code 技能定义
│   └── markdown-organizer/
│       ├── SKILL.md                  # 技能说明（Claude 执行时的指导）
│       └── scripts/                   # Python 脚本
│           ├── organize_markdown.py   # 图片下载与格式美化
│           └── enhance_content.py     # 内容增强（备用，AI 智能思考替代）
├── img/                              # 项目资源
│   └── f5339aeb70e245d782f288ba17ace4ff.jpg  # 插件预览图
└── README.md                         # 项目说明文档
```

## 🔄 更新机制

插件支持自动更新检查：

- **自动检查**：每次 Claude Code 会话启动时自动检查新版本
- **手动更新**：
  ```bash
  /plugin update organize_markdown@markdown-organizer
  ```


## ⚙️ 依赖

```bash
pip install requests
```

依赖会在插件安装后自动检查和安装。

## 🗑️ 卸载

```bash
# Claude Code 卸载
/plugin uninstall organize_markdown@markdown-organizer

# Gemini CLI 卸载
gemini skills uninstall markdown-organizer
```

## ❓ 常见问题

**Q: 图片下载失败？**
A: 检查网络连接和 URL 是否可访问

**Q: 相对路径图片无法处理？**
A: 提供 `base_url` 参数，如：`/markdown-organizer @file.md https://example.com/article`

**Q: Claude 生成的学习目标不符合预期？**
A: Claude 会根据文档内容智能生成，您可以在生成后手动调整

**Q: 如何跳过 AI 内容增强？**
A: 当前版本 AI 增强是默认行为，如需纯脚本处理可使用 `organize_markdown.py` 单独运行

## 📝 许可证

MIT License

## 🔗 相关链接

- [GitHub 仓库](https://github.com/xiaodizi/organize_markdown_skills)
- [问题反馈](https://github.com/xiaodizi/organize_markdown_skills/issues)
