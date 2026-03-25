#!/usr/bin/env python3
"""
Format markdown to WeChat official account style.
- Adds emojis to chapter titles
- Optimizes paragraph spacing
- Enhances emphasis on key points
- Improves list formatting
"""

import re
import argparse
import os
from pathlib import Path
from typing import Optional

# Common emoji mappings for different sections
SECTION_EMOJIS = {
    r'概览|概述|简介|介绍|前言': '🔍',
    r'背景|相关': '📚',
    r'原理|理论|概念': '💡',
    r'方法|步骤|流程|实践': '⚙️',
    r'最佳实践|推荐': '✨',
    r'示例|案例': '📝',
    r'问题|故障|错误|坑': '⚠️',
    r'解决|方案': '✅',
    r'对比|比较': '⚖️',
    r'总结|结语': '🎯',
    r'参考|链接': '🔗',
    r'安装|部署': '🚀',
    r'配置|设置': '⚙️',
    r'使用|用法': '📖',
    r'特性|功能': '🌟',
    r'性能|优化': '⚡',
    r'安全|风险': '🔒',
    r'测试|验证': '🧪',
    r'架构|设计': '🏗️',
    r'实现|开发': '👨‍💻',
    r'未来|展望': '🔮',
}

# Default emojis by heading level
DEFAULT_EMOJIS = {
    1: '📌',
    2: '⚡',
    3: '🔸',
    4: '▫️',
}

def add_emoji_to_heading(line: str) -> str:
    """Add appropriate emoji to heading based on content."""
    if not line.startswith('#'):
        return line

    # Get heading level
    match = re.match(r'^#+', line)
    level = len(match.group()) if match else 1
    heading_text = line.lstrip('# ').strip()

    # Check if already has emoji
    if any(c in heading_text for c in ['🔍', '📚', '💡', '⚙️', '✨', '📝', '⚠️', '✅', '⚖️', '🎯', '🔗', '🚀', '⚡', '🌟', '🔒', '🧪', '🏗️', '👨‍💻', '🔮', '📌', '🔸', '▫️']):
        return line

    # Find matching emoji
    emoji = None
    for pattern, e in SECTION_EMOJIS.items():
        if re.search(pattern, heading_text, re.IGNORECASE):
            emoji = e
            break

    # Use default if no match
    if emoji is None:
        emoji = DEFAULT_EMOJIS.get(level, '')

    if emoji:
        return f"{'#' * level} {emoji} {heading_text}"
    else:
        return line

def enhance_key_points(content: str) -> str:
    """Enhance emphasis on key points by ensuring proper bolding."""
    # Make sure important keywords are bolded if they are already marked
    # This just ensures spacing is correct
    patterns = [
        # Ensure single space around bold
        (r'\*\*(\w+)\*\*', r'**\1**'),
    ]
    for pattern, repl in patterns:
        content = re.sub(pattern, repl, content)
    return content

def fix_paragraph_spacing(content: str) -> str:
    """Ensure proper paragraph spacing."""
    # Remove multiple blank lines (more than 2)
    content = re.sub(r'\n\s*\n\s*\n+', r'\n\n', content)

    # Ensure single newline after headings
    content = re.sub(r'(^#+.*)\n+', r'\1\n\n', content, flags=re.MULTILINE)

    return content

def optimize_list_formatting(content: str) -> str:
    """Optimize list formatting for better readability."""
    # Ensure proper spacing around lists
    content = re.sub(r'([^\n])\n(- |\d+\. )', r'\1\n\n\2', content)

    # Ensure proper spacing after list items
    content = re.sub(r'(- .*)\n([^- \d])', r'\1\n\n\2', content)

    return content

def generate_toc(content: str) -> str:
    """Generate table of contents from headings."""
    toc_lines = ['## 📑 本文目录\n\n']
    heading_pattern = re.compile(r'^(#+) (.+)$', re.MULTILINE)

    for match in heading_pattern.finditer(content):
        level = len(match.group(1))
        heading = match.group(2).lstrip('🔍📚💡⚙️✨📝⚠️✅⚖️🎯🔗🚀⚡🌟🔒🧪🏗️👨‍💻🔮📌🔸▫️ ').strip()
        if level == 1:
            toc_lines.append(f'- [{heading}](#{heading.lower().replace(" ", "-")})\n')
        elif level == 2:
            toc_lines.append(f'  - [{heading}](#{heading.lower().replace(" ", "-")})\n')

    if len(toc_lines) > 2:  # If we have more than just the title
        # Check if TOC already exists
        if '## 📑 本文目录' not in content and '本文目录' not in content:
            # Insert TOC after first heading (title)
            first_heading_match = list(heading_pattern.finditer(content))
            if first_heading_match:
                first_heading = first_heading_match[0]
                end_pos = first_heading.end()
                toc_content = ''.join(toc_lines) + '\n'
                content = content[:end_pos] + '\n' + toc_content + content[end_pos:]
    return content

def format_wechat_markdown(input_path: str, output_path: Optional[str] = None, add_toc: bool = True) -> str:
    """Format markdown to WeChat style."""
    # Read input
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Process line by line for headings
    lines = content.split('\n')
    processed_lines = []
    for line in lines:
        if line.startswith('#'):
            processed_lines.append(add_emoji_to_heading(line))
        else:
            processed_lines.append(line)
    content = '\n'.join(processed_lines)

    # Apply other enhancements
    content = enhance_key_points(content)
    content = optimize_list_formatting(content)
    content = fix_paragraph_spacing(content)

    # Generate TOC if requested
    if add_toc:
        content = generate_toc(content)

    # Final spacing fix
    content = fix_paragraph_spacing(content)

    # Write output
    if output_path is None:
        stem = Path(input_path).stem
        output_path = str(Path(input_path).parent / f"{stem}_wechat.md")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Formatted: {input_path} → {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Format markdown to WeChat official account style')
    parser.add_argument('input', help='Input markdown file path')
    parser.add_argument('output', nargs='?', help='Output file path (optional)')
    parser.add_argument('--no-toc', action='store_true', help='Skip table of contents generation')
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    add_toc = not args.no_toc

    if not os.path.exists(input_path):
        print(f"❌ Error: File not found: {input_path}")
        exit(1)

    result = format_wechat_markdown(input_path, output_path, add_toc)
    print(f"\nDone! Output saved to: {result}")

if __name__ == '__main__':
    main()
