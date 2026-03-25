# 更新日志

## v1.0.7 - 2026-03-25

### 新增
- ✨ **三个独立系统命令**，支持 `npx` 直接调用：
  - `markdown-organizer` - 组织和美化 Markdown 文档
  - `url-to-markdown` - 将 URL 转换为 Markdown 文档
  - `wechat-format` - 将 Markdown 转换为微信公众号 HTML 格式
- ✨ **新增 wechat-format 技能**：
  - 转换 Markdown 为微信公众号样式 HTML
  - 使用微信公众号风格 CSS
  - 支持标题自动添加 Emoji
  - 内置一键复制按钮
  - 输出可直接粘贴到微信编辑器
- ✨ **完整中文帮助信息**：
  - 三个命令全部使用自定义参数解析
  - 帮助信息完全中文输出
  - 支持 `--help`/`-h`
- ✨ 新增 `Dockerfile` 和 `docker-compose.yml` 支持沙箱测试
- ✨ 新增 `requirements.txt` Python 依赖清单

### 修改
- 📝 更新 `README.md` 添加完整命令行使用说明
- 📝 更新帮助信息格式，三个命令结构统一
- 🐛 修复 `markdown-organizer.js` 脚本文件名错误（从 markdown_organizer 修正为 organize_markdown）
- 🎨 更新 `.gitignore` 添加 `settings.json` 和 `__pycache__` 忽略

## v1.0.6 - 2026-03-20

### 新增
- ✨ 新增 url-to-markdown 技能
- ✨ 支持直接从 URL 转换网页为 Markdown
- ✨ 支持 JS 动态页面渲染（Playwright）
- ✨ 新增依赖 beautifulsoup4 和 html2text

### 修改
- 📝 更新 README 文档

## v1.0.5 - 2026-03-xx

### 新增
- ✨ 新增 npm/npx 安装方式支持
- ✨ 新增 `npx skills-add-organize-markdown` 命令
- ✨ 优化安装体验

## v1.0.4 - 2026-03-xx

### 新增
- ✨ 新增 Gemini CLI 技能支持
- ✨ 直接执行命令 `/organize`

## v1.0.2 - 2026-03-xx

### 新增
- ✨ Claude 智能思考生成学习目标和前置知识
- ✨ 自动更新检查

## v1.0.1 - 2026-03-xx

### 优化
- 🎨 精简目录结构
- 🎨 优化变量加载路径

## v1.0.0 - 2026-03-xx

### 初始发布
- ✨ markdown-organizer 技能
- ✨ 图片本地化
- ✨ 格式美化
- ✨ AI 内容增强
