#!/usr/bin/env node
/**
 * wechat-format CLI
 * Markdown 转换为微信公众号 HTML 格式 - 命令行入口
 * 功能：转换为微信公众号样式的 HTML，支持一键复制
 */

const { spawn } = require('child_process');
const path = require('path');

// 获取 Python 脚本路径
const scriptPath = path.join(__dirname, '../skills/wechat-format/scripts/markdown_to_wechat.py');

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
  console.error('  pip install markdown');
  process.exit(1);
});

proc.on('close', (code) => {
  process.exit(code || 0);
});
