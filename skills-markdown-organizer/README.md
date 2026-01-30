# Markdown Organizer Skill

 Claude Code 技能，用于组织和美化从网页复制的 Markdown 文档。

## 功能

- 自动下载 Markdown 中的图片到本地 `img` 文件夹
- 更新图片引用为本地路径
- 美化 Markdown 格式

## 安装

```bash
# 添加市场源
/plugin marketplace add xiaodizi/organize_markdown_skills

# 安装技能
/plugin install markdown-organizer@xiaodizi-organize_markdown_skills
```

## 使用

```
/markdown-organizer @文件路径
```

## 手动安装

```bash
# 克隆仓库
git clone https://github.com/xiaodizi/organize_markdown_skills.git

# 创建技能目录
mkdir -p ~/.claude/skills/markdown-organizer

# 复制文件
cp -r organize_markdown_skills/skills-markdown-organizer/* ~/.claude/skills/markdown-organizer/

# 安装依赖
pip install requests
```

## 依赖

- Python 3.10+
- `requests` 库

```bash
pip install requests
```
