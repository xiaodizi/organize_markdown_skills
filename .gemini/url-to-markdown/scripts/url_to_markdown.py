#!/usr/bin/env python3
"""
URL 到 Markdown 转换工具

功能：
1. 从 URL 获取网页内容
2. 将 HTML 转换为清晰的 Markdown
3. 提取并下载图片到本地 img 文件夹
4. 更新 Markdown 中的图片引用为本地路径
5. 美化 Markdown 格式
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
    parsed = urllib.parse.urlparse(url)
    path = parsed.path

    ext = os.path.splitext(path)[1].lower()
    if not ext or len(ext) > 10:
        ext = ".jpg"

    url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()[:12]
    return f"{url_hash}{ext}"


def download_image(url: str, img_dir: Path) -> str | None:
    """下载图片到本地目录"""
    try:
        filename = sanitize_filename(url)
        local_path = img_dir / filename

        if local_path.exists():
            return filename

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        with open(local_path, "wb") as f:
            f.write(response.content)

        print(f"  ✅ 下载成功: {filename}")
        return filename

    except Exception as e:
        print(f"  ❌ 下载失败: {url} - {e}")
        return None


def extract_and_download_images(content: str, base_url: str, img_dir: Path) -> str:
    """提取并下载图片，返回更新后的内容"""
    img_pattern = r"!\[([^\]]*)\]\(([^)]+)\)"

    def replace_image(match):
        alt_text = match.group(1)
        img_url = match.group(2).strip()

        if not img_url.startswith(("http://", "https://")):
            if img_url.startswith("/"):
                parsed_base = urllib.parse.urlparse(base_url)
                img_url = f"{parsed_base.scheme}://{parsed_base.netloc}{img_url}"
            else:
                img_url = urllib.parse.urljoin(base_url, img_url)

        print(f"\n📥 处理图片: {img_url}")
        filename = download_image(img_url, img_dir)

        if filename:
            return f"![{alt_text}](./img/{filename})"
        else:
            return match.group(0)

    updated_content = re.sub(img_pattern, replace_image, content)
    return updated_content


def fetch_webpage(url: str) -> tuple[str, str]:
    """获取网页内容"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"🌐 获取网页: {url}")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    return response.text, url


def html_to_markdown(html: str, base_url: str) -> str:
    """将 HTML 转换为 Markdown"""
    # 尝试使用 html2text
    try:
        import html2text

        print("🔄 使用 html2text 转换...")
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.ignore_emphasis = False
        h.body_width = 0
        h.mark_code = True
        h.single_line_break = False
        markdown = h.handle(html)
        return markdown
    except ImportError:
        pass

    # 尝试使用 BeautifulSoup
    try:
        from bs4 import BeautifulSoup

        print("🔄 使用 BeautifulSoup 提取文本...")
        soup = BeautifulSoup(html, "html.parser")

        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        main_content = soup.find("main") or soup.find("article") or soup.body

        if main_content:
            text = main_content.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)

        text = re.sub(r"\n{3,}", "\n\n", text)
        return text
    except ImportError:
        pass

    # 如果都没有，返回原始 HTML
    print("⚠️  没有找到 html2text 或 BeautifulSoup，返回原始 HTML")
    return f"<!-- HTML content from {base_url} -->\n\n```html\n{html[:5000]}...\n```"


def beautify_markdown(content: str) -> str:
    """美化 markdown 格式"""
    lines = content.split("\n")
    beautified_lines = []

    for i, line in enumerate(lines):
        if re.match(r"^#{1,6}\s+", line):
            if i > 0 and lines[i - 1].strip():
                beautified_lines.append("")
            beautified_lines.append(line)
            if i < len(lines) - 1 and lines[i + 1].strip():
                beautified_lines.append("")
        else:
            beautified_lines.append(line)

    content = "\n".join(beautified_lines)

    content = re.sub(r"^(\s*)\*\s+", r"\1- ", content, flags=re.MULTILINE)
    content = re.sub(r"^(\s*)\+\s+", r"\1- ", content, flags=re.MULTILINE)

    content = re.sub(r"(\n)(```[^\n]*)(\n)", r"\1\n\2\3", content)

    content = re.sub(r"\n{3,}", "\n\n", content)

    content = "\n".join(line.rstrip() for line in content.split("\n"))

    return content


def generate_output_path(url: str, output_path: str | None = None) -> Path:
    """生成输出文件路径"""
    if output_path:
        path = Path(output_path)
        if not path.suffix:
            path = path.with_suffix(".md")
        return path.resolve()

    parsed = urllib.parse.urlparse(url)
    path_parts = parsed.path.strip("/").split("/")

    filename = path_parts[-1] if path_parts else "index"
    if not filename:
        filename = "index"

    filename = re.sub(r"[^\w\-]", "_", filename)
    if not filename.endswith(".md"):
        filename = f"{filename}.md"

    return Path.cwd() / filename


def url_to_markdown(url: str, output_path: str | None = None) -> None:
    """
    将 URL 转换为 Markdown 文档

    Args:
        url: 网页 URL
        output_path: 输出文件路径（可选）
    """
    html, base_url = fetch_webpage(url)

    markdown = html_to_markdown(html, base_url)

    output_file = generate_output_path(url, output_path)
    work_dir = output_file.parent

    work_dir.mkdir(parents=True, exist_ok=True)

    img_dir = work_dir / "img"
    img_dir.mkdir(exist_ok=True)

    print(f"\n📁 工作目录: {work_dir}")
    print(f"📁 图片目录: {img_dir}")

    print("\n🔍 搜索并下载图片...")
    markdown = extract_and_download_images(markdown, base_url, img_dir)

    print("\n✨ 美化 Markdown 格式...")
    markdown = beautify_markdown(markdown)

    print(f"\n💾 写入文件: {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"\n✅ 完成！文件已保存到: {output_file}")


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python url_to_markdown.py <URL> [输出文件路径]")
        print("示例: python url_to_markdown.py https://example.com/post/123")
        print("示例: python url_to_markdown.py https://example.com/post/123 ./docs/article.md")
        print("\n依赖: pip install requests beautifulsoup4 html2text")
        sys.exit(1)

    url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        url_to_markdown(url, output_path)
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
