# Markdown Organizer

组织和美化从网页复制的 Markdown 文档，自动下载图片到本地并更新引用。

![](./img/f5339aeb70e245d782f288ba17ace4ff.jpg)

## 更新

- 精简了目录结果，修改变量加载路径。不再将skills复制到Claude Code的skills文件夹作为技能加载。
- 增加了一个文档增强脚本，会对文档识别，增加学习目标和前置知识，以及调整更适合新手学习和查看的文档的格式。
- 调整了一下启动命令(只是改了个名字)。

## 功能

- **图片本地化**：自动下载 Markdown 中的图片到 `img` 文件夹
- **路径更新**：将图片引用从网络 URL 更新为本地路径
- **格式美化**：标题空行、列表规范化、删除多余空行

## 安装

### 方式一：从 GitHub 安装（推荐）

```bash
# 1. 添加市场源
/plugin marketplace add xiaodizi/organize_markdown_skills

# 2. 安装插件
/plugin install organize_markdown@markdown-organizer
```

### 方式二：本地安装

```bash
# 添加本地市场源
/plugin marketplace add /path/to/organize_markdown_skills

# 安装插件
/plugin install organize_markdown@markdown-organizer
```

### 安装依赖

```bash
pip install requests
```

## 使用

### 命令触发

```
/markdown-organizer @文件路径
```

**示例**：
```
/markdown-organizer @/Users/lei.fu/documents/article.md
/markdown-organizer @article.md https://example.com/post/123
```

### 自然语言触发

- "@文件路径 帮我美化文档"
- "处理这个 markdown 文件"

## 项目结构

```
organize_markdown_skills/
├── .claude-plugin/           # 插件配置
│   ├── plugin.json
│   └── marketplace.json
├── commands/                 # 命令快捷方式
│   └── markdown-organizer.md
├── scripts/                  # Python 脚本
│   ├── organize_markdown.py
│   └── enhance_content.py
├── hooks/                    # 插件钩子
│   ├── hooks.json
│   └── check-deps.sh
├── skills/                   # 技能定义
│   ├── markdown-organizer/
│   └── markdown-organizer-standalone/
└── README.md
```

## 卸载

```bash
/plugin uninstall organize_markdown@markdown-organizer
```

## 故障排除

- **图片下载失败**：检查网络连接和 URL 可访问性
- **路径解析错误**：确保文件路径正确，相对路径图片提供原网页 URL
- **依赖库未安装**：运行 `pip install requests`
