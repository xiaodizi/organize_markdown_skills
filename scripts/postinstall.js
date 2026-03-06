#!/usr/bin/env node

/**
 * Post-install script
 * npm install 后自动运行
 */


// 颜色输出
const colors = {
  green: (text) => `\x1b[32m${text}\x1b[0m`,
  yellow: (text) => `\x1b[33m${text}\x1b[0m`,
  blue: (text) => `\x1b[34m${text}\x1b[0m`,
};

console.log('');
console.log(colors.green('╔═══════════════════════════════════════════════════════════════╗'));
console.log(colors.green('║         ✅ Markdown Organizer 安装成功！                        ║'));
console.log(colors.green('╚═══════════════════════════════════════════════════════════════╝'));
console.log('');

console.log(colors.blue('下一步：'));
console.log('');
console.log('  运行以下命令完成技能安装：');
console.log(colors.yellow('    npx skills-add-organize-markdown'));
console.log('');
console.log('  或者：');
console.log(colors.yellow('    npx organize-markdown-skills skills:add'));
console.log('');
console.log(colors.blue('更多信息：'));
console.log('  GitHub: https://github.com/xiaodizi/organize_markdown_skills');
console.log('');
