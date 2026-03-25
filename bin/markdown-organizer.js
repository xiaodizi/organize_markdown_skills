#!/usr/bin/env node
/**
 * markdown-organizer CLI
 * 组织和美化 Markdown 文档 - 命令行入口
 * 功能：自动下载图片到本地、更新图片引用、美化格式
 */

const { spawn } = require('child_process');
const path = require('path');

// 获取 Python 脚本路径
const scriptPath = path.join(__dirname, '../skills/markdown-organizer/scripts/organize_markdown.py');

// 传递所有参数给 Python 脚本
const args = [scriptPath, ...process.argv.slice(2)];

// 执行 Python 脚本
const proc = spawn(process.env.PYTHON || 'python3', args, {
  stdio: 'inherit',
  cwd: process.cwd()
});

proc.on('error', (err) => {
  console.error('启动失败：', err.message);
  console.error('');
  console.error('请确保已安装 Python 3，并且安装了依赖：');
  console.error('  pip install requests beautifulsoup4');
  process.exit(1);
});

proc.on('close', (code) => {
  process.exit(code || 0);
});
