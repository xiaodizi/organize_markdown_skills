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
import yaml
import hashlib
import subprocess
import urllib.parse
from pathlib import Path

import requests


def sanitize_filename(url: str, prefix: str = "") -> str:
    """根据 URL 生成安全的文件名，可选前缀"""
    # 解析 URL 获取路径部分
    parsed = urllib.parse.urlparse(url)
    path = parsed.path

    # 获取文件扩展名
    ext = os.path.splitext(path)[1].lower()
    if not ext or len(ext) > 10:
        ext = ".jpg"  # 默认扩展名

    # 使用 URL 的 MD5 作为文件名（避免文件名过长或包含非法字符）
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

        # 优先检查带前缀的文件名
        if local_path.exists():
            print(f"  ℹ️ 文件已存在: {filename}")
            return filename

        # 如果带前缀的文件不存在，检查无前缀的旧文件
        if prefix:
            filename_without_prefix = sanitize_filename(url, prefix="")
            old_path = img_dir / filename_without_prefix
            if old_path.exists():
                print(f"  ℹ️ 使用已存在的文件: {filename_without_prefix}")
                # 文件存在但没有前缀，返回旧的文件名用于引用
                # 这样至少图片不会损坏
                return filename_without_prefix

        # 下载图片
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # 保存图片
        with open(local_path, "wb") as f:
            f.write(response.content)

        print(f"  ✅ 下载成功: {filename}")
        return filename

    except Exception as e:
        print(f"  ❌ 下载失败: {url} - {e}")
        return None


def extract_and_download_images(
    content: str, base_url: str, img_dir: Path, prefix: str = ""
) -> str:
    """提取并下载图片，返回更新后的内容。可选前缀用于图片文件名"""
    # 匹配 markdown 图片语法: ![alt](url)
    img_pattern = r"!\[([^\]]*)\]\(([^)]+)\)"

    def replace_image(match):
        alt_text = match.group(1)
        img_url = match.group(2).strip()

        # 处理相对 URL
        if not img_url.startswith(("http://", "https://", "/")):
            # 是相对路径，可能需要与 base_url 组合
            img_url = urllib.parse.urljoin(base_url, img_url)

        # 下载图片
        print(f"\n📥 处理图片: {img_url}")
        filename = download_image(img_url, img_dir, prefix=prefix)

        if filename:
            # 返回本地引用
            return f"![{alt_text}](./img/{filename})"
        else:
            # 下载失败，保留原引用
            return match.group(0)

    # 替换所有图片引用
    updated_content = re.sub(img_pattern, replace_image, content)
    return updated_content


def resolve_file_path(file_path: str | Path) -> Path:
    """
    解析文件路径，支持相对路径

    如果文件不存在，尝试在当前目录和常见位置查找
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    # 如果是绝对路径，直接返回
    if file_path.is_absolute():
        if file_path.exists():
            return file_path
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 相对路径，尝试在不同位置查找
    search_paths = [
        Path.cwd(),  # 当前工作目录
        Path.home(),  # 用户主目录
    ]

    # 从环境变量获取可能的路径
    if "CLAUDE_WORKING_DIR" in os.environ:
        search_paths.insert(0, Path(os.environ["CLAUDE_WORKING_DIR"]))

    # 尝试在当前目录和父目录查找
    for base_path in search_paths:
        full_path = base_path / file_path
        if full_path.exists():
            return full_path.resolve()

    # 尝试递归搜索（最多3层深度）
    for base_path in search_paths:
        for root, dirs, files in os.walk(base_path):
            # 限制搜索深度
            level = root.replace(str(base_path), "").count(os.sep)
            if level >= 3:
                dirs[:] = []  # 不再深入
                continue

            if file_path.name in files:
                return Path(root) / file_path.name

    # 列出所有找到的 .md 文件供参考
    md_files = []
    for base_path in search_paths:
        for root, dirs, files in os.walk(base_path):
            level = root.replace(str(base_path), "").count(os.sep)
            if level >= 2:
                dirs[:] = []
                continue
            for f in files:
                if f.endswith(".md"):
                    md_files.append(str(Path(root) / f))

    error_msg = (
        f"无法找到文件: {file_path}\n搜索路径: {[str(p) for p in search_paths]}\n"
    )
    if md_files:
        error_msg += f"\n找到的 Markdown 文件:\n" + "\n".join(md_files[:10])
    error_msg += f"\n\n请提供绝对路径或确保文件在当前工作目录中"

    raise FileNotFoundError(error_msg)


def extract_title_from_frontmatter(content: str) -> str:
    """从 frontmatter 中提取 title 字段"""
    try:
        frontmatter_match = re.match(
            r"^---\s*\n(.*?)\n---\s*(?:\n|$)", content, re.DOTALL
        )
        if not frontmatter_match:
            return ""

        frontmatter_text = frontmatter_match.group(1)
        frontmatter_data = yaml.safe_load(frontmatter_text)

        if frontmatter_data and isinstance(frontmatter_data, dict):
            title = frontmatter_data.get("title", "")
            return str(title).strip() if title else ""
    except Exception as e:
        print(f"  ⚠️ 提取 title 失败: {e}")

    return ""


def clean_duplicate_metadata(content: str) -> str:
    """
    清理 frontmatter 中的重复元数据

    当 title 被提取并生成为一级标题后，frontmatter 中的 title 字段就成了重复的
    此函数删除 frontmatter 中的 title 字段
    """
    try:
        frontmatter_match = re.match(
            r"^---\s*\n(.*?)\n---\s*(?:\n|$)", content, re.DOTALL
        )
        if not frontmatter_match:
            return content

        frontmatter_text = frontmatter_match.group(1)
        end_pos = frontmatter_match.end()

        # 解析 YAML
        frontmatter_data = yaml.safe_load(frontmatter_text)

        if not frontmatter_data or not isinstance(frontmatter_data, dict):
            return content

        # 如果没有 title 字段，直接返回
        if "title" not in frontmatter_data:
            return content

        # 删除 title 字段
        del frontmatter_data["title"]

        # 重新生成 frontmatter
        new_frontmatter_text = yaml.dump(
            frontmatter_data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        ).rstrip()

        # 构建新内容
        rest_content = content[end_pos:]
        new_content = f"---\n{new_frontmatter_text}\n---\n{rest_content}"

        print("  ✅ 已删除重复的 title 字段")
        return new_content

    except Exception as e:
        print(f"  ⚠️ 清理元数据失败: {e}")
        return content


def fix_yaml_frontmatter(content: str) -> str:
    """
    检测并修复 YAML frontmatter 中的缩进问题

    常见问题：
    - 列表项缩进不一致，导致列表项无法被正确识别
    - 例如：tags 列表的最后一项没有正确缩进到 tags 键下

    返回修复后的内容
    """
    # 检测 frontmatter 部分
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", content, re.DOTALL)
    if not frontmatter_match:
        return content

    frontmatter_text = frontmatter_match.group(1)

    # 尝试解析 YAML，看是否有错误
    try:
        yaml.safe_load(frontmatter_text)
        # 如果成功解析，说明格式正确
        return content
    except yaml.YAMLError as e:
        # YAML 解析失败，尝试自动修复
        print(f"  ⚠️ 检测到 YAML 格式问题: {str(e)[:50]}...")

        # 修复策略：规范化缩进
        fixed_frontmatter = fix_yaml_indentation(frontmatter_text)

        # 验证修复后的格式
        try:
            yaml.safe_load(fixed_frontmatter)
            print("  ✅ YAML 格式已自动修复")
            # 替换原有的 frontmatter
            end_pos = frontmatter_match.end()
            return "---\n" + fixed_frontmatter + "\n---\n" + content[end_pos:]
        except yaml.YAMLError:
            # 修复失败，返回原始内容
            print("  ⚠️ YAML 修复失败，保持原样")
            return content


def fix_yaml_indentation(frontmatter_text: str) -> str:
    """
    修复 YAML frontmatter 的缩进问题

    主要问题：列表项缩进不一致
    例如：
    tags:
      - item1
      - item2
    - item3  # 这行缩进错误，应该缩进到 tags 下

    修复方法：
    1. 识别键值对的缩进级别
    2. 确保该键对应的列表项都有相同的缩进
    """
    lines = frontmatter_text.split("\n")
    fixed_lines = []

    # 追踪当前的缩进上下文
    key_indents = {}  # 记录每个键的缩进级别
    current_key = None
    current_indent = 0

    for line in lines:
        if not line.strip():
            # 空行保持原样
            fixed_lines.append(line)
            continue

        # 计算当前行的缩进
        indent = len(line) - len(line.lstrip())
        stripped = line.lstrip()

        # 检测键值对（key:）
        if re.match(r"^[^:\s]+:\s*", stripped):
            key = re.match(r"^([^:]+):", stripped).group(1).strip()
            current_key = key
            current_indent = indent
            key_indents[key] = indent
            fixed_lines.append(line)

        # 检测列表项（- item）
        elif stripped.startswith("-"):
            if current_key and current_indent is not None:
                # 列表项应该缩进在其所属键下
                expected_indent = current_indent + 2

                # 如果缩进不对，修正它
                if indent != expected_indent and indent <= current_indent:
                    # 这是一个缩进错误的列表项
                    fixed_line = " " * expected_indent + stripped
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        else:
            # 其他行保持原样
            fixed_lines.append(line)

    return "\n".join(fixed_lines)


def beautify_markdown(content: str) -> str:
    """美化 markdown 格式"""
    # 1. 标题层级规范化
    # 确保标题前后有空行
    lines = content.split("\n")
    beautified_lines = []

    for i, line in enumerate(lines):
        # 处理标题
        if re.match(r"^#{1,6}\s+", line):
            # 标题前添加空行（如果前面不是空行）
            if i > 0 and lines[i - 1].strip():
                beautified_lines.append("")
            beautified_lines.append(line)
            # 标题后添加空行（如果后面不是空行）
            if i < len(lines) - 1 and lines[i + 1].strip():
                beautified_lines.append("")
        else:
            beautified_lines.append(line)

    content = "\n".join(beautified_lines)

    # 2. 列表格式化
    # 统一使用 "- " 作为列表标记
    content = re.sub(r"^(\s*)\*\s+", r"\1- ", content, flags=re.MULTILINE)
    content = re.sub(r"^(\s*)\+\s+", r"\1- ", content, flags=re.MULTILINE)

    # 3. 代码块规范化
    # 确保代码块前后有空行
    content = re.sub(r"(\n)(```[^\n]*)(\n)", r"\1\n\2\3", content)

    # 4. 删除多余的空行（最多保留2个连续空行）
    content = re.sub(r"\n{3,}", "\n\n", content)

    # 5. 去除行尾空格
    content = "\n".join(line.rstrip() for line in content.split("\n"))

    return content


def organize_markdown(file_path: str | Path, base_url: str = "") -> None:
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
    img_dir = work_dir / "img"
    img_dir.mkdir(exist_ok=True)

    print(f"📁 工作目录: {work_dir}")
    print(f"📁 图片目录: {img_dir}")

    # 读取 markdown 文件
    print(f"\n📖 读取文件: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 从 frontmatter 中提取 title 作为图片前缀
    title_prefix = extract_title_from_frontmatter(content)
    if title_prefix:
        print(f"📌 图片前缀: {title_prefix}")

    # 修复 YAML frontmatter 格式问题
    print("\n🔧 检查 YAML 格式...")
    content = fix_yaml_frontmatter(content)

    # 清理重复的元数据（删除 frontmatter 中的 title 字段）
    print("\n🧹 清理重复元数据...")
    content = clean_duplicate_metadata(content)

    # 提取并下载图片
    print("\n🔍 搜索并下载图片...")
    content = extract_and_download_images(
        content, base_url, img_dir, prefix=title_prefix
    )

    # 美化 markdown
    print("\n✨ 美化 Markdown 格式...")
    content = beautify_markdown(content)

    # 写回文件
    print(f"\n💾 写入文件: {file_path}")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    # 调用 enhance_content.py 进行内容增强
    print("\n📝 内容增强...")
    script_dir = Path(__file__).parent
    enhance_script = script_dir / "enhance_content.py"
    if enhance_script.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(enhance_script), "--enhance", str(file_path)],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                print("  ✅ 内容增强完成")
            else:
                print(f"  ⚠️ 内容增强提示: {result.stderr.strip()}")
        except Exception as e:
            print(f"  ⚠️ 内容增强跳过: {e}")
    else:
        print("  ⚠️ enhance_content.py 未找到，跳过内容增强")

    print("\n✅ 完成！")


def show_help():
    """显示帮助信息"""
    print("用法: markdown-organizer <markdown文件> [base_url]")
    print("")
    print("组织和美化 Markdown 文档，自动下载网络图片到本地并更新引用")
    print("")
    print("参数:")
    print("  <markdown文件>      输入 Markdown 文件路径 (必填)")
    print(
        "  [base_url]          基础 URL，用于处理相对路径图片（可选，当图片链接是相对路径时需要提供原网页 URL）"
    )
    print("")
    print("示例:")
    print("  markdown-organizer article.md")
    print("  markdown-organizer article.md https://example.com/article")


def main():
    """命令行入口"""
    import sys

    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h"]:
        show_help()
        if len(sys.argv) < 2:
            print("\n❌ 错误: 缺少必填参数: markdown文件")
            sys.exit(1)
        else:
            sys.exit(0)

    file_path = sys.argv[1]
    base_url = sys.argv[2] if len(sys.argv) > 2 else ""

    # 解析文件路径
    try:
        resolved_path = resolve_file_path(file_path)
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)

    organize_markdown(resolved_path, base_url)


if __name__ == "__main__":
    main()
