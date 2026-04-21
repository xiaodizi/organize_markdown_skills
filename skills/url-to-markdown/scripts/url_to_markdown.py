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


def sanitize_filename(url: str, prefix: str = "") -> str:
    """根据 URL 生成安全的文件名，可选前缀"""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path

    ext = os.path.splitext(path)[1].lower()
    if not ext or len(ext) > 10:
        ext = ".jpg"

    url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()[:12]
    
    if prefix:
        # 清理前缀中的非法字符，保留字母、数字、中文和下划线
        prefix = re.sub(r"[^\w\u4e00-\u9fff-]", "_", prefix).strip("_")
        if len(prefix) > 30:
            prefix = prefix[:30]
        return f"{prefix}_{url_hash}{ext}"
    
    return f"{url_hash}{ext}"


def download_image(url: str, img_dir: Path, prefix: str = "") -> str | None:
    """下载图片到本地目录，可选前缀"""
    try:
        filename = sanitize_filename(url, prefix=prefix)
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


def extract_and_download_images(content: str, base_url: str, img_dir: Path, prefix: str = "") -> str:
    """提取并下载图片，返回更新后的内容。可选前缀用于图片文件名"""
    img_pattern = r"!\[([^\]]*)\]\(([^)]+)\)"

    def replace_image(match):
        alt_text = match.group(1)
        img_url = match.group(2).strip()

        # 跳过 data:image base64 占位图片
        if img_url.startswith("data:"):
            # 移除空占位图片
            return ""

        if not img_url.startswith(("http://", "https://")):
            if img_url.startswith("/"):
                parsed_base = urllib.parse.urlparse(base_url)
                img_url = f"{parsed_base.scheme}://{parsed_base.netloc}{img_url}"
            else:
                img_url = urllib.parse.urljoin(base_url, img_url)

        print(f"\n📥 处理图片: {img_url[:80]}{'...' if len(img_url) > 80 else ''}")
        filename = download_image(img_url, img_dir, prefix=prefix)

        if filename:
            return f"![{alt_text}](./img/{filename})"
        else:
            return match.group(0)

    updated_content = re.sub(img_pattern, replace_image, content)
    # 移除因为删除图片产生的空行
    updated_content = re.sub(r"\n\s*\n\s*\n", "\n\n", updated_content)
    return updated_content


def fetch_webpage(
    url: str,
    render: bool = False,
    render_wait_for: str | None = None,
    render_timeout: int = 30000,
    render_wait_until: str = "networkidle",
) -> tuple[str, str]:
    """获取网页内容。

    如果 `render` 为 True，尝试使用 Playwright 在无头浏览器中渲染页面后再获取完整 HTML。
    否则使用 requests 直接获取页面源 HTML。
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"🌐 获取网页: {url}")

    if render:
        try:
            from playwright.sync_api import sync_playwright

            print("🔎 使用 headless 浏览器渲染页面（Playwright）...")
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                try:
                    page.set_default_navigation_timeout(render_timeout)
                    page.goto(url, wait_until=render_wait_until, timeout=render_timeout)
                    if render_wait_for:
                        page.wait_for_selector(render_wait_for, timeout=render_timeout)
                    content = page.content()
                finally:
                    browser.close()

            return content, url
        except Exception as e:
            print(
                f"⚠️ 渲染失败（Playwright）：{e}，回退到常规请求模式。\n若要启用完整渲染，请安装 Playwright 并运行 `playwright install`。"
            )

    # 非渲染模式或回退
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    return response.text, url


def clean_html_content(html: str) -> str:
    """清理 HTML，去除导航、侧边栏、推荐、评论、广告等无用内容"""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return html

    soup = BeautifulSoup(html, "html.parser")

    # 修复懒加载图片：将 data-src / data-url 等复制到 src 属性
    # 这样 html2text 才能正确获取图片 URL
    lazy_attrs = ["data-src", "data-url", "data-original", "data-img-src"]
    for img in soup.find_all("img"):
        for attr in lazy_attrs:
            if img.has_attr(attr) and img[attr].strip().startswith(("http://", "https://")):
                img["src"] = img[attr]
                break

    # 要删除的标签和常见无用内容选择器
    selectors_to_remove = [
        # 脚本和样式
        "script", "style", "noscript", "iframe",
        # 导航和页脚
        "nav", "footer", "header", "sidebar",
        # 广告和推荐区域（常见类名和ID）
        ".ad", ".ads", ".advertisement", ".banner",
        "#footer", "#header", "#nav", "#sidebar", "#sidebar-wrapper",
        ".footer", ".header", ".navbar", ".navigation", ".side-bar",
        ".related", ".recommend", ".recommendation", ".recommended",
        ".popular", ".hot", ".trending",
        ".comment", ".comments", "#comment", "#comments",
        ".share", ".sharing", ".social",
        ".author-card", ".author-info", ".profile-card",
        ".copyright", ".license", ".powered-by",
        ".toutiao__footer", ".article-footer", ".article-comment",
        ".article-related", ".recommend-feed", ".hot-board",
        ".video-card", ".related-news", ".news-recommend",
        "#reptilde-beg", "#reptilde-end",  # 折叠区域
        ".back-to-top", ".go-top",
        # 头条特定
        ".nav-bar", ".header-nav", "t-nav", "tt-feed",
        ".bottom-bar", ".article-share",
        ".article-meta", ".article-detail__meta",
        "#bottomContainer", ".article-toolbar",
    ]

    for selector in selectors_to_remove:
        if selector.startswith(".") or selector.startswith("#"):
            # CSS 选择器
            elements = soup.select(selector)
            for elem in elements:
                elem.decompose()
        else:
            # 标签名
            for elem in soup.find_all(selector):
                elem.decompose()

    # 尝试找到主要内容区域
    main_content = None

    # 优先找 article 标签
    article = soup.find("article")
    if article:
        main_content = article

    # 找不到就找 main 标签
    if not main_content:
        main_content = soup.find("main")

    # 找不到就找常见的内容容器类名
    if not main_content:
        content_candidates = [
            ".article-content", ".article-body", ".post-content", ".post-body",
            ".entry-content", ".entry-body", ".content", ".main-content",
            ".article-main", ".main-body", "#article-content", "#main-content",
            ".rich_media", ".rich_media_content",  # 微信公众号
            ".article-content-inner", ".toutiao-content",  # 头条
            ".article-detail__content", ".article-content-wrap",
        ]
        for candidate in content_candidates:
            found = soup.select_one(candidate)
            if found:
                main_content = found
                break

    # 如果找到了主要内容，就用它
    if main_content:
        # 检查这个容器是否真的包含内容（至少有一些文字或图片）
        text_len = len(main_content.get_text(strip=True))
        img_count = len(main_content.find_all('img'))
        # 如果容器太小空的，可能找错了，fallback 到 body
        if text_len > 100 or img_count > 0:
            # 清理空标签，但是保留：
            # - img 标签（img 本身没有文本，但不是空标签）
            # - pre/code 标签（代码块，即使看起来空也可能是格式问题不删）
            # - 任何包含子元素的容器都不删（只删除真正叶子节点的空标签）
            for elem in main_content.find_all():
                if elem.name in ['img', 'pre', 'code']:
                    continue  # 图片和代码永远不删
                # 只删除：没有文字，也没有任何子元素 的真正空标签
                # 这样可以避免误删除包含代码块的外层容器
                text_len = len(elem.get_text(strip=True))
                child_count = len(elem.find_all())
                if text_len == 0 and child_count == 0:
                    elem.decompose()
            return str(main_content)

    # 找不到合适容器，返回清理后的整个 body
    body = soup.body
    if body:
        return str(body)

    return html


def html_to_markdown(html: str, base_url: str) -> str:
    """将 HTML 转换为 Markdown"""
    # 先清理 HTML，去除无用内容
    html = clean_html_content(html)

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

    # 尝试使用 BeautifulSoup 直接提取文本
    try:
        from bs4 import BeautifulSoup

        print("🔄 使用 BeautifulSoup 提取文本...")
        soup = BeautifulSoup(html, "html.parser")

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


def url_to_markdown(
    url: str,
    output_path: str | None = None,
    render: bool = False,
    render_wait_for: str | None = None,
    render_timeout: int = 30000,
    render_wait_until: str = "networkidle",
) -> None:
    """
    将 URL 转换为 Markdown 文档

    Args:
        url: 网页 URL
        output_path: 输出文件路径（可选）
    """
    html, base_url = fetch_webpage(
        url,
        render=render,
        render_wait_for=render_wait_for,
        render_timeout=render_timeout,
        render_wait_until=render_wait_until,
    )

    markdown = html_to_markdown(html, base_url)

    output_file = generate_output_path(url, output_path)
    work_dir = output_file.parent

    work_dir.mkdir(parents=True, exist_ok=True)

    img_dir = work_dir / "img"
    img_dir.mkdir(exist_ok=True)

    print(f"\n📁 工作目录: {work_dir}")
    print(f"📁 图片目录: {img_dir}")

    # 从文档标题中提取前缀（第一个 # 标题）
    title_prefix = ""
    title_match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    if title_match:
        title_prefix = title_match.group(1).strip()
        print(f"📌 图片前缀: {title_prefix}")

    print("\n🔍 搜索并下载图片...")
    markdown = extract_and_download_images(markdown, base_url, img_dir, prefix=title_prefix)

    print("\n✨ 美化 Markdown 格式...")
    markdown = beautify_markdown(markdown)

    print(f"\n💾 写入文件: {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"\n✅ 完成！文件已保存到: {output_file}")


def show_help():
    """显示帮助信息"""
    print("用法: url-to-markdown <网址> [输出文件] [选项]")
    print("")
    print("将 URL 转换为 Markdown 文档（支持可选的无头浏览器渲染）")
    print("")
    print("参数:")
    print("  <网址>                目标网页 URL (必填)")
    print("  [输出文件]            输出文件路径（可选，默认自动生成）")
    print("")
    print("选项:")
    print("  --render              使用无头浏览器渲染页面（Playwright），以抓取 JS 渲染后的内容")
    print("  --render-wait-for SELECTOR   渲染时等待某个 CSS 选择器出现再抓取（可选）")
    print("  --render-wait-until STRATEGY  渲染时页面导航等待策略: load, domcontentloaded, networkidle (默认: networkidle)")
    print("  --render-timeout MILLIS      渲染超时时间（毫秒，默认 30000）")
    print("")
    print("示例:")
    print("  url-to-markdown https://example.com/article.html")
    print("  url-to-markdown https://example.com/article.html output.md")
    print("  url-to-markdown https://react-site.com/article output.md --render")
    print("  url-to-markdown https://react-site.com/article output.md --render --render-wait-for \".article-content\"")

def main():
    import sys

    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h"]:
        show_help()
        sys.exit(0)

    url = sys.argv[1]
    output = None
    render = False
    render_wait_for = None
    render_wait_until = "networkidle"
    render_timeout = 30000

    # 解析选项
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in ["--help", "-h"]:
            show_help()
            sys.exit(0)
        elif arg == "--render":
            render = True
            i += 1
        elif arg == "--render-wait-for" and i + 1 < len(sys.argv):
            render_wait_for = sys.argv[i + 1]
            i += 2
        elif arg == "--render-wait-until" and i + 1 < len(sys.argv):
            render_wait_until = sys.argv[i + 1]
            if render_wait_until not in ["load", "domcontentloaded", "networkidle"]:
                print(f"❌ 错误: --render-wait-until 必须是: load, domcontentloaded, networkidle")
                sys.exit(1)
            i += 2
        elif arg == "--render-timeout" and i + 1 < len(sys.argv):
            try:
                render_timeout = int(sys.argv[i + 1])
            except ValueError:
                print("❌ 错误: --render-timeout 必须是整数")
                sys.exit(1)
            i += 2
        elif output is None:
            output = arg
            i += 1
        else:
            print(f"❌ 错误: 未知参数: {arg}")
            show_help()
            sys.exit(1)

    try:
        url_to_markdown(
            url,
            output,
            render=render,
            render_wait_for=render_wait_for,
            render_timeout=render_timeout,
            render_wait_until=render_wait_until,
        )
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
