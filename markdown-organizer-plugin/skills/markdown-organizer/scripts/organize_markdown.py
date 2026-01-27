#!/usr/bin/env python3
"""
Markdown 文档组织和图片下载工具

功能：
1. 提取 markdown 文件中的图片 URL
2. 下载图片到本地 img 文件夹
3. 更新 markdown 中的图片引用为本地路径
4. 美化 markdown 格式
"""

import os
import re
import sys
import hashlib
import urllib.parse
from pathlib import Path

import requests


def sanitize_filename(url: str) -> str:
    """根据 URL 生成安全的文件名"""
    # 解析 URL 获取路径部分
    parsed = urllib.parse.urlparse(url)
    path = parsed.path

    # 获取文件扩展名
    ext = os.path.splitext(path)[1].lower()
    if not ext or len(ext) > 10:
        ext = '.jpg'  # 默认扩展名

    # 使用 URL 的 MD5 作为文件名（避免文件名过长或包含非法字符）
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:12]
    return f"{url_hash}{ext}"


def download_image(url: str, img_dir: Path) -> str | None:
    """下载图片到本地目录"""
    try:
        filename = sanitize_filename(url)
        local_path = img_dir / filename

        # 如果文件已存在，直接返回
        if local_path.exists():
            return filename

        # 下载图片
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # 保存图片
        with open(local_path, 'wb') as f:
            f.write(response.content)

        print(f"  ✅ 下载成功: {filename}")
        return filename

    except Exception as e:
        print(f"  ❌ 下载失败: {url} - {e}")
        return None


def extract_and_download_images(content: str, base_url: str, img_dir: Path) -> str:
    """提取并下载图片，返回更新后的内容"""
    # 匹配 markdown 图片语法: ![alt](url)
    img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    def replace_image(match):
        alt_text = match.group(1)
        img_url = match.group(2).strip()

        # 处理相对 URL
        if not img_url.startswith(('http://', 'https://', '/')):
            # 是相对路径，可能需要与 base_url 组合
            img_url = urllib.parse.urljoin(base_url, img_url)

        # 下载图片
        print(f"\n📥 处理图片: {img_url}")
        filename = download_image(img_url, img_dir)

        if filename:
            # 返回本地引用
            return f'![{alt_text}](./img/{filename})'
        else:
            # 下载失败，保留原引用
            return match.group(0)

    # 替换所有图片引用
    updated_content = re.sub(img_pattern, replace_image, content)
    return updated_content


def beautify_markdown(content: str) -> str:
    """美化 markdown 格式"""
    # 1. 标题层级规范化
    # 确保标题前后有空行
    lines = content.split('\n')
    beautified_lines = []

    for i, line in enumerate(lines):
        # 处理标题
        if re.match(r'^#{1,6}\s+', line):
            # 标题前添加空行（如果前面不是空行）
            if i > 0 and lines[i-1].strip():
                beautified_lines.append('')
            beautified_lines.append(line)
            # 标题后添加空行（如果后面不是空行）
            if i < len(lines) - 1 and lines[i+1].strip():
                beautified_lines.append('')
        else:
            beautified_lines.append(line)

    content = '\n'.join(beautified_lines)

    # 2. 列表格式化
    # 统一使用 "- " 作为列表标记
    content = re.sub(r'^(\s*)\*\s+', r'\1- ', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)\+\s+', r'\1- ', content, flags=re.MULTILINE)

    # 3. 代码块规范化
    # 确保代码块前后有空行
    content = re.sub(r'(\n)(```[^\n]*)(\n)', r'\1\n\2\3', content)

    # 4. 删除多余的空行（最多保留2个连续空行）
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 5. 去除行尾空格
    content = '\n'.join(line.rstrip() for line in content.split('\n'))

    return content


def organize_markdown(file_path: str | Path, base_url: str = '') -> None:
    """
    组织和美化 markdown 文件

    Args:
        file_path: markdown 文件路径
        base_url: 原文章页面的 URL（用于处理相对路径的图片）
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    work_dir = file_path.parent

    # 创建 img 文件夹
    img_dir = work_dir / 'img'
    img_dir.mkdir(exist_ok=True)

    print(f"📁 工作目录: {work_dir}")
    print(f"📁 图片目录: {img_dir}")

    # 读取 markdown 文件
    print(f"\n📖 读取文件: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取并下载图片
    print("\n🔍 搜索并下载图片...")
    content = extract_and_download_images(content, base_url, img_dir)

    # 美化 markdown
    print("\n✨ 美化 Markdown 格式...")
    content = beautify_markdown(content)

    # 写回文件
    print(f"\n💾 写入文件: {file_path}")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\n✅ 完成！")


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python organize_markdown.py <markdown文件路径> [base_url]")
        print("示例: python organize_markdown.py article.md https://example.com/article")
        sys.exit(1)

    file_path = sys.argv[1]
    base_url = sys.argv[2] if len(sys.argv) > 2 else ''

    organize_markdown(file_path, base_url)


if __name__ == '__main__':
    main()
