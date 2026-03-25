# Docker 沙箱测试安装文档

## 启动容器

```bash
# 在当前项目目录执行
docker-compose run --rm wechat-test bash
```

## 在容器中安装 Claude Code CLI

```bash
# 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

## 安装本地插件

进入容器后，在 `/app` 目录（就是你的项目）执行：

```bash
# 在 Claude Code 中运行安装命令
claude
```

进入 Claude Code 交互后，运行：

```
/plugin install /app
```

这会从本地路径安装插件，安装完成后重启 Claude Code 就能看到 `wechat-format` 命令了。

## 测试新命令

安装完成重启后，测试命令：

```
/wechat-format 7617405322227139135.md
```

## 预期结果

- 命令应该能被正确识别
- 脚本会将 Markdown 转换为 HTML
- 生成 `7617405322227139135_wechat.html` 输出文件

## 退出容器

```bash
# 在容器内
exit

# 清理容器（可选）
docker-compose down
```

## 环境说明

- Python 3.11 + 已安装依赖：`markdown requests beautifulsoup4 html2text`
- Node.js 18 + npm
- git + curl
- 当前项目通过 volume 挂载到 `/app`，修改会同步到本地

---
