# Markdown Organizer 技能

## 技能介绍

Markdown Organizer 是一个专门用于处理从网页复制的 Markdown 文档的工具。它能够自动下载文档中引用的图片到本地，并更新图片引用路径，同时美化 Markdown 格式，让文档更符合阅读和存储规范。

### 主要功能

- **图片本地化**：自动识别 Markdown 中的图片 URL，下载到本地 `img` 文件夹
- **路径更新**：将图片引用从网络 URL 更新为本地路径
- **格式美化**：优化 Markdown 格式，提升可读性
- **智能处理**：支持处理相对路径图片，可指定源网页 URL 作为参考

## 项目结构

```
organize_markdown_skills/
├── markdown-organizer/           # Claude Code 技能目录
│   ├── SKILL.md                  # 技能说明文档
│   ├── scripts/                  # 脚本目录
│   │   ├── organize_markdown.py  # 格式美化脚本
│   │   └── enhance_content.py    # 内容增强脚本
│   ├── commands/                 # 命令快捷方式
│   │   └── markdown-organizer.md
│   ├── hooks/                    # 插件钩子
│   │   ├── hooks.json            # 钩子配置
│   │   └── check-deps.sh         # 依赖检查脚本
│   └── .claude-plugin/           # 插件元数据
│       ├── plugin.json           # 插件配置
│       └── marketplace.json      # Marketplace 配置
└── README.md                     # 本文档
```

## 安装方法

### 通过 Marketplace 安装（推荐）

#### 1. 添加市场源

```bash
/plugin marketplace add xiaodizi/organize_markdown_skills
```

#### 2. 安装插件

```bash
/plugin install markdown-organizer@markdown-organizer
```

### 手动安装 Python 依赖

插件安装后，需要在系统上安装 `requests` 库：

```bash
pip install requests
```

**注意**：插件会在每次会话开始时检查依赖是否已安装，如果未安装会提示您。

### 验证安装

执行以下命令验证插件是否成功安装：

```bash
# 检查插件列表
/plugin list

# 验证 Python 依赖
pip show requests
```

## 卸载方法

### 使用 Claude Code 卸载命令（推荐）

```bash
/plugin uninstall markdown-organizer@markdown-organizer
```

### 完全清理

1. **卸载插件**
   ```bash
   /plugin uninstall markdown-organizer@markdown-organizer
   ```

2. **卸载依赖库**（可选）
   ```bash
   pip uninstall -y requests
   ```

### 验证卸载

执行以下命令验证卸载是否成功：

```bash
# 检查插件列表（应无输出）
/plugin list | grep markdown-organizer
```

如果命令没有输出，说明卸载完成。

## 使用方法

### 基本使用

#### 1. 通过命令直接触发

在 Claude Code 中使用以下格式：

```
/markdown-organizer @文件路径
```

**示例**：
```
/markdown-organizer @/Users/lei.fu/documents/article.md
```

#### 2. 自然语言触发

您可以使用以下方式触发技能：

```
@/path/to/file.md 帮我美化文档
```

或

```
帮我处理这个 Markdown 文件，图片需要下载到本地：@article.md
```

### 高级选项

#### 指定源网页 URL

如果 Markdown 中的图片使用相对路径，可以指定原网页 URL 帮助解析：

```
@article.md 美化这个文档，原页面是 https://example.com/post/123
```

#### 手动运行脚本

您也可以直接运行 Python 脚本来处理文件：

```bash
cd /path/to/markdown-organizer
python3 scripts/organize_markdown.py /path/to/your/document.md [optional-base-url]
```

**参数说明**：
- `/path/to/your/document.md`：需要处理的 Markdown 文件路径（必需）
- `[optional-base-url]`：原网页 URL（可选，用于解析相对路径图片）

### 处理过程

执行技能后，会自动完成以下操作：

1. 在 Markdown 文件所在目录创建 `img` 文件夹（如不存在）
2. 下载所有图片到 `img` 文件夹（使用 MD5 哈希命名避免冲突）
3. 更新 Markdown 中的图片引用为本地路径
4. 美化 Markdown 格式（标题格式、列表规范、代码块优化等）

### 输出结果

处理完成后，会显示以下信息：
- 处理的文件路径
- 下载的图片数量
- 格式美化的统计信息
- 是否有错误或警告

## 示例

### 输入文件样例

```markdown
# 标题

这是一篇从网页复制的文章，包含图片：

![示例图片](https://example.com/images/sample.jpg)

## 内容

- 列表项1
- 列表项2
```

### 处理后文件

```markdown
# 标题

这是一篇从网页复制的文章，包含图片：

![示例图片](./img/abc123def456.jpg)

## 内容

- 列表项1
- 列表项2
```

同时会在同目录下创建 `img` 文件夹，并包含下载的图片 `abc123def456.jpg`。

## 故障排除

### 常见问题

1. **图片下载失败**
   - 检查网络连接
   - 确保图片 URL 可访问
   - 检查文件权限

2. **路径解析错误**
   - 确保文件路径正确
   - 如果是相对路径图片，尝试提供原网页 URL

3. **依赖库未安装**
   - 检查 `pip show requests` 是否已安装
   - 运行 `pip install requests`

4. **插件未找到**
   - 检查 Marketplace 源是否已添加
   - 尝试重新安装插件

## 技术细节

### 核心脚本

主处理脚本位置：
```
markdown-organizer/scripts/organize_markdown.py
```

### 技能配置

技能定义文件：
```
markdown-organizer/SKILL.md
```

### 插件配置

插件元数据文件：
```
markdown-organizer/.claude-plugin/plugin.json
markdown-organizer/.claude-plugin/marketplace.json
```

### 钩子配置

检查依赖的钩子配置：
```
markdown-organizer/hooks/hooks.json
markdown-organizer/hooks/check-deps.sh
```

## 反馈与支持

如有问题或建议，请通过以下方式反馈：

1. 查看脚本输出的错误信息
2. 检查文件权限和路径
3. 确保网络连接正常
4. 提交 Issue 到项目仓库

## 许可证

MIT License
