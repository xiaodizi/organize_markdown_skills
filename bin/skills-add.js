#!/usr/bin/env node

/**
 * Skills Add CLI
 * 用于将 organize-markdown 技能安装到 Claude Code 或其他支持的平台
 *
 * Usage:
 *   npx skills-add-organize-markdown
 *   npx organize-markdown-skills skills:add
 */

const fs = require('fs');
const path = require('path');

const PACKAGE_NAME = 'organize-markdown-skills';
const SKILL_NAME = 'markdown-organizer';

// 颜色输出
const colors = {
  green: (text) => `\x1b[32m${text}\x1b[0m`,
  yellow: (text) => `\x1b[33m${text}\x1b[0m`,
  blue: (text) => `\x1b[34m${text}\x1b[0m`,
  red: (text) => `\x1b[31m${text}\x1b[0m`,
};

function log(message) {
  console.log(message);
}

function info(message) {
  console.log(colors.blue(`[INFO] ${message}`));
}

function success(message) {
  console.log(colors.green(`[SUCCESS] ${message}`));
}

function warn(message) {
  console.log(colors.yellow(`[WARN] ${message}`));
}

function error(message) {
  console.error(colors.red(`[ERROR] ${message}`));
}

// 获取当前包的安装路径
function getPackagePath() {
  // 尝试多种方式找到包的安装位置
  const possiblePaths = [
    __dirname,
    path.dirname(require.main?.filename || __dirname),
    process.cwd(),
  ];

  for (const p of possiblePaths) {
    const pkgPath = path.join(p, 'package.json');
    if (fs.existsSync(pkgPath)) {
      const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
      if (pkg.name === PACKAGE_NAME) {
        return p;
      }
    }
  }

  // 如果是通过 npx 运行，可能在 node_modules 中
  try {
    return path.dirname(require.resolve(`${PACKAGE_NAME}/package.json`));
  } catch {
    return __dirname;
  }
}

// 检测 Claude Code 配置目录
function detectClaudeConfigDir() {
  const home = process.env.HOME || process.env.USERPROFILE;
  if (!home) {
    return null;
  }

  const claudeDir = path.join(home, '.claude');
  if (fs.existsSync(claudeDir)) {
    return claudeDir;
  }
  return null;
}

// 检测是否在 Claude Code 环境中
function isInClaudeCode() {
  return process.env.CLAUDE_CODE === '1' ||
         process.argv.some(arg => arg.includes('claude')) ||
         detectClaudeConfigDir() !== null;
}

// 复制技能文件到 Claude Code
async function installToClaudeCode() {
  const claudeDir = detectClaudeConfigDir();
  if (!claudeDir) {
    warn('未找到 Claude Code 配置目录，尝试使用插件方式安装');
    return false;
  }

  info('检测到 Claude Code 环境');

  // 检查是否支持 /plugin 命令
  try {
    // 尝试通过插件方式安装
    log('');
    log('请在 Claude Code 中运行以下命令来安装插件：');
    log('');
    log(colors.green(`  /plugin marketplace add xiaodizi/organize_markdown_skills`));
    log(colors.green(`  /plugin install organize_markdown@${SKILL_NAME}`));
    log('');
    return true;
  } catch (e) {
    warn('无法自动安装到 Claude Code');
    return false;
  }
}

// 显示安装说明
function showManualInstructions(packagePath) {
  log('');
  log(colors.yellow('╔═══════════════════════════════════════════════════════════════╗'));
  log(colors.yellow('║                Markdown Organizer 技能安装指南                  ║'));
  log(colors.yellow('╚═══════════════════════════════════════════════════════════════╝'));
  log('');

  log(colors.blue('【 Claude Code 安装方式 】'));
  log('');
  log('方式一：插件市场安装（推荐）');
  log(colors.green('  1. /plugin marketplace add xiaodizi/organize_markdown_skills'));
  log(colors.green('  2. /plugin install organize_markdown@markdown-organizer'));
  log('');

  log('方式二：从本地安装');
  log(colors.green(`  /plugin install ${packagePath}`));
  log('');

  log(colors.blue('【 Gemini CLI 安装方式 】'));
  log('');
  log(colors.green('  gemini skills install https://github.com/xiaodizi/organize_markdown_skills.git'));
  log('');

  log(colors.blue('【 使用方法 】'));
  log('');
  log('在 Claude Code 中：');
  log(colors.green('  /markdown-organizer @/path/to/your/file.md'));
  log('');

  log('在 Gemini CLI 中：');
  log(colors.green('  /organize-markdown @/path/to/your/file.md'));
  log('');

  log(colors.blue('【 项目地址 】'));
  log('  GitHub: https://github.com/xiaodizi/organize_markdown_skills');
  log('');
}

// 主函数
async function main() {
  log('');
  log(colors.green('╔═══════════════════════════════════════════════════════════════╗'));
  log(colors.green('║              Markdown Organizer Skills Installer                ║'));
  log(colors.green('╚═══════════════════════════════════════════════════════════════╝'));
  log('');

  const packagePath = getPackagePath();
  info(`包路径: ${packagePath}`);

  // 尝试自动检测并安装
  let installed = false;

  if (isInClaudeCode()) {
    installed = await installToClaudeCode();
  }

  // 如果没有自动安装，显示手动说明
  if (!installed) {
    showManualInstructions(packagePath);
  }

  success('安装准备完成！');
  log('');
}

main().catch((err) => {
  error(`安装失败: ${err.message}`);
  console.error(err);
  process.exit(1);
});
