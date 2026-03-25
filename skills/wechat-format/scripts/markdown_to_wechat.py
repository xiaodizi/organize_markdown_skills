#!/usr/bin/env python3
"""
Convert Markdown to WeChat Official Account HTML format.
- Uses WeChat-style CSS matching popular article formatting
- Includes one-click copy button
- Output ready-to-paste HTML
"""

import re
import argparse
import os
import html
from pathlib import Path
from typing import Optional

# Try to import markdown, install if not available
try:
    import markdown
    HAVE_MARKDOWN = True
except ImportError:
    HAVE_MARKDOWN = False

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

WECHAT_CSS = """
/* WeChat Official Account Style */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", "PingFang SC", Hiragino Sans GB, "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 1.8;
    color: #333333;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 100%;
    padding: 15px 20px;
    box-sizing: border-box;
}

/* Cover image */
.cover-image {
    width: 100%;
    margin: 0 auto 20px;
    text-align: center;
}

.cover-image img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
}

/* Headings */
h1 {
    font-size: 22px;
    font-weight: bold;
    color: #1a1a1a;
    text-align: center;
    margin: 30px 0 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #f0f0f0;
}

h2 {
    font-size: 20px;
    font-weight: bold;
    color: #2c3e50;
    margin: 25px 0 15px;
    padding-left: 0;
}

h3 {
    font-size: 18px;
    font-weight: bold;
    color: #34495e;
    margin: 20px 0 10px;
}

h4 {
    font-size: 17px;
    font-weight: bold;
    color: #4a4a4a;
    margin: 18px 0 8px;
}

/* Paragraphs */
p {
    margin: 12px 0;
    text-align: justify;
    letter-spacing: 0.5px;
}

/* Lists */
ul, ol {
    margin: 15px 0;
    padding-left: 25px;
}

li {
    margin: 8px 0;
    line-height: 1.8;
}

/* Code blocks */
pre {
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
    margin: 15px 0;
    border-left: 4px solid #58a6ff;
}

code {
    background-color: #f6f8fa;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 14px;
    color: #d73a49;
}

pre code {
    background-color: transparent;
    color: #24292e;
    padding: 0;
}

/* Blockquotes */
blockquote {
    border-left: 4px solid #58a6ff;
    padding-left: 15px;
    margin: 15px 0;
    color: #6a737d;
    background-color: #f8f9fa;
    padding: 10px 15px;
    border-radius: 0 4px 4px 0;
}

/* Links */
a {
    color: #58a6ff;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* Images */
img {
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    margin: 15px auto;
    display: block;
}

/* Tables */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 15px 0;
    overflow: hidden;
    border-radius: 6px;
}

th {
    background-color: #f6f8fa;
    font-weight: bold;
    text-align: left;
}

th, td {
    padding: 10px 15px;
    border: 1px solid #eaecef;
}

/* Strong/bold */
strong {
    color: #1a1a1a;
    font-weight: bold;
}

/* Horizontal rule */
hr {
    border: 0;
    height: 1px;
    background-color: #eaecef;
    margin: 30px 0;
}

/* TOC */
.toc {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 15px 20px;
    margin: 20px 0;
}

.toc h2 {
    margin-top: 0;
    font-size: 18px;
}

.toc ul {
    margin: 0;
    padding-left: 20px;
}

.toc li {
    margin: 5px 0;
}

/* Copy button */
.copy-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
}

.copy-button {
    background-color: #07c160;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 15px;
    font-weight: bold;
    box-shadow: 0 2px 8px rgba(7, 193, 96, 0.3);
}

.copy-button:hover {
    background-color: #06ad56;
}

.copy-button.copied {
    background-color: #58a6ff;
}

/* Footer note */
.footer-note {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #eaecef;
    color: #999;
    font-size: 14px;
    text-align: center;
}

/* Responsive */
@media screen and (max-width: 600px) {
    body {
        font-size: 15px;
    }

    h1 {
        font-size: 20px;
    }

    h2 {
        font-size: 18px;
    }

    .copy-container {
        top: 10px;
        right: 10px;
    }

    .copy-button {
        padding: 8px 16px;
        font-size: 14px;
    }
}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{css}
    </style>
</head>
<body>
    <div class="copy-container">
        <button class="copy-button" onclick="copyContent()" id="copyBtn">📋 一键复制</button>
    </div>
    <div class="container" id="content">
{content}
    </div>
    <script>
    function copyContent() {{
        const content = document.getElementById('content');
        const range = document.createRange();
        range.selectNode(content);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        document.execCommand('copy');
        window.getSelection().removeAllRanges();

        const btn = document.getElementById('copyBtn');
        const originalText = btn.textContent;
        btn.textContent = '✅ 已复制';
        btn.classList.add('copied');
        setTimeout(() => {{
            btn.textContent = originalText;
            btn.classList.remove('copied');
        }}, 2000);
    }}
    </script>
</body>
</html>
"""

def add_emoji_to_heading_markdown(line: str) -> str:
    """Add appropriate emoji to heading in markdown."""
    if not line.startswith('#'):
        return line

    match = re.match(r'^#+', line)
    level = len(match.group()) if match else 1
    heading_text = line.lstrip('# ').strip()

    # Check if already has emoji
    if any(c in heading_text for c in ['🔍', '📚', '💡', '⚙️', '✨', '📝', '⚠️', '✅', '⚖️', '🎯', '🔗', '🚀', '⚡', '🌟', '🔒', '🧪', '🏗️', '👨‍💻', '🔮', '📌', '🔸', '▫️']):
        return line

    emoji = None
    for pattern, e in SECTION_EMOJIS.items():
        if re.search(pattern, heading_text, re.IGNORECASE):
            emoji = e
            break

    if emoji is None:
        emoji = DEFAULT_EMOJIS.get(level, '')

    if emoji:
        return f"{'#' * level} {emoji} {heading_text}"
    else:
        return line

def process_markdown_with_emoji(content: str) -> str:
    """Add emojis to all headings in markdown."""
    lines = content.split('\n')
    processed = []
    for line in lines:
        if line.startswith('#'):
            processed.append(add_emoji_to_heading_markdown(line))
        else:
            processed.append(line)
    return '\n'.join(processed)

def enhance_key_points(content: str) -> str:
    """Ensure proper bold formatting."""
    content = re.sub(r'\*\*(\w+)\*\*', r'**\1**', content)
    return content

def fix_paragraph_spacing(content: str) -> str:
    """Fix paragraph spacing in markdown."""
    content = re.sub(r'\n\s*\n\s*\n+', r'\n\n', content)
    content = re.sub(r'(^#+.*)\n+', r'\1\n\n', content, flags=re.MULTILINE)
    return content

def optimize_list_formatting(content: str) -> str:
    """Optimize list spacing."""
    content = re.sub(r'([^\n])\n(- |\d+\. )', r'\1\n\n\2', content)
    content = re.sub(r'(- .*)\n([^- \d])', r'\1\n\n\2', content)
    return content

def convert_markdown_to_wechat_html(input_path: str, output_path: Optional[str] = None, add_emoji: bool = True) -> str:
    """Convert markdown to WeChat HTML format."""
    if not HAVE_MARKDOWN:
        raise ImportError("需要安装 markdown 库: pip install markdown")

    # Read input
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Process markdown
    if add_emoji:
        content = process_markdown_with_emoji(content)
    content = enhance_key_points(content)
    content = optimize_list_formatting(content)
    content = fix_paragraph_spacing(content)

    # Convert to HTML
    html_content = markdown.markdown(content, extensions=['extra', 'codehilite', 'tables'])

    # Get title from first h1
    title_match = re.search(r'^#\s+.+$', content, re.MULTILINE)
    title = "WeChat Article"
    if title_match:
        title = title_match.group(0).lstrip('# ').strip()
        # Remove emoji from title
        title = re.sub(r'^[🔍📚💡⚙️✨📝⚠️✅⚖️🎯🔗🚀⚡🌟🔒🧪🏗️👨‍💻🔮📌🔸▫️]\s+', '', title)

    # Wrap with template
    full_html = HTML_TEMPLATE.format(
        title=html.escape(title),
        css=WECHAT_CSS,
        content=html_content
    )

    # Write output
    if output_path is None:
        stem = Path(input_path).stem
        output_path = str(Path(input_path).parent / f"{stem}_wechat.html")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"✅ Converted: {input_path} → {output_path}")
    print(f"ℹ️  Open {output_path} in browser, click '一键复制' to copy content, then paste directly into WeChat Official Account editor.")
    return output_path

def show_help():
    """显示帮助信息"""
    print("用法: wechat-format <输入Markdown> [输出HTML] [选项]")
    print("")
    print("将 Markdown 转换为微信公众号 HTML 格式，输出可直接复制粘贴到微信编辑器")
    print("")
    print("参数:")
    print("  <输入Markdown>       输入 Markdown 文件路径 (必填)")
    print("  [输出HTML]          输出 HTML 文件路径（可选，默认生成 <输入>_wechat.html）")
    print("")
    print("选项:")
    print("  --no-emoji          不在标题中添加 Emoji 图标")
    print("")
    print("示例:")
    print("  wechat-format article.md")
    print("  wechat-format article.md article.html")
    print("  wechat-format article.md article.html --no-emoji")

def main():
    import sys

    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h"]:
        show_help()
        sys.exit(0)

    input_path = sys.argv[1]
    output_path = None
    add_emoji = True

    # 解析选项
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in ["--help", "-h"]:
            show_help()
            sys.exit(0)
        elif arg == "--no-emoji":
            add_emoji = False
            i += 1
        elif output_path is None:
            output_path = arg
            i += 1
        else:
            print(f"❌ 错误: 未知参数: {arg}")
            show_help()
            sys.exit(1)

    if not HAVE_MARKDOWN:
        print("❌ 错误: 需要安装 markdown 库，请运行:")
        print("   pip install markdown")
        sys.exit(1)

    if not os.path.exists(input_path):
        print(f"❌ 错误: 文件不存在: {input_path}")
        sys.exit(1)

    result = convert_markdown_to_wechat_html(input_path, output_path, add_emoji)
    print(f"\n完成！输出文件: {result}")

if __name__ == '__main__':
    main()
