#!/usr/bin/env node

/**
 * Markdown Organizer CLI
 * 命令行工具入口
 */

const path = require('path');

function showHelp() {
  console.log(`
Markdown Organizer CLI

用法:
  organize-markdown [命令] [选项]

命令:
  skills:add          安装技能到 Claude Code/Gemini CLI
  help                显示帮助信息

示例:
  organize-markdown skills:add
  npx organize-markdown-skills skills:add
`);
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'skills:add':
    case 'install':
    case 'add': {
      const skillsAddPath = path.join(__dirname, 'skills-add.js');
      require(skillsAddPath);
      break;
    }

    case 'help':
    case '--help':
    case '-h':
    default:
      showHelp();
      break;
  }
}

main().catch((err) => {
  console.error('错误:', err);
  process.exit(1);
});
