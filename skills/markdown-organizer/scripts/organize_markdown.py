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

        # 跳过已经是本地图片的引用（保持原样）
        # 检查是否已经是本地存储的图片路径
        if img_url.startswith(("./img/", "../img/", "/img/")):
            print(f"  ⏭️  跳过已存储的本地图片: {img_url}")
            return match.group(0)

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


def ensure_h1_title(content: str) -> str:
    """
    确保文档有一级标题 (# 标题)

    如果没有一级标题，从 frontmatter 的 title 字段生成
    这是处理 Web Clipper 元数据的一部分
    """
    # 检查是否已经有一级标题
    if re.search(r"^#\s+", content, re.MULTILINE):
        return content

    # 检查是否有 frontmatter
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", content, re.DOTALL)

    if not frontmatter_match:
        # 没有 frontmatter，无法生成标题
        return content

    # 从 frontmatter 提取 title
    frontmatter_text = frontmatter_match.group(1)
    try:
        frontmatter_data = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter_data, dict):
            return content

        title = frontmatter_data.get("title", "").strip()
        if not title or title == "未命名":
            # title 无意义，无法生成一级标题
            return content

        # 在 frontmatter 后插入一级标题
        end_pos = frontmatter_match.end()
        h1_line = f"\n# {title}\n"

        result = content[:end_pos] + h1_line + content[end_pos:]
        print(f"  ✅ 从 title 生成一级标题: # {title}")
        return result
    except Exception as e:
        print(f"  ⚠️ 生成一级标题失败: {e}")
        return content


def ensure_h1_title_after_enhancements(content: str) -> str:
    """
    确保文档有一级标题，位置在所有增强内容块之后
    """
    # 检查是否已经有一级标题
    if re.search(r"^# \S", content, re.MULTILINE):
        return content

    # 检查是否有 frontmatter
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", content, re.DOTALL)

    if not frontmatter_match:
        return content

    # 从 frontmatter 提取 title
    frontmatter_text = frontmatter_match.group(1)
    try:
        frontmatter_data = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter_data, dict):
            return content

        title = frontmatter_data.get("title", "").strip()
        if not title or title == "未命名":
            return content

        lines = content.split("\n")
        frontmatter_end_line = content[: frontmatter_match.end()].count("\n")

        # 已知的增强内容块标题
        enhancement_blocks = [
            "## 学习目标",
            "## 前置知识",
            "## 前置条件",
            "## 摘要",
            "## 概述",
            "## 常见问题",
            "## FAQ",
            "## 知识图谱",
        ]

        # 查找最后一个增强块在内容中的位置
        last_enhancement_pos = -1
        for block in enhancement_blocks:
            pos = content.rfind(block)
            if pos > frontmatter_match.end() and pos > last_enhancement_pos:
                last_enhancement_pos = pos

        if last_enhancement_pos == -1:
            # 没有增强块，在第一个非空行前插入
            insert_line = frontmatter_end_line + 1
            for i in range(frontmatter_end_line + 1, len(lines)):
                if lines[i].strip():
                    insert_line = i
                    break
        else:
            # 找到最后一个增强块
            # 从该块之后开始，查找第一个非##、非空、非###、非列表项的行
            # 该行前面就是插入位置
            start_search_from = content.find("\n", last_enhancement_pos)
            if start_search_from == -1:
                start_search_from = len(content)
            else:
                start_search_from += 1

            remaining_content = content[start_search_from:]
            remaining_lines = remaining_content.split("\n")

            insert_line = len(lines)  # 默认在末尾
            for i, line in enumerate(remaining_lines):
                # 空行继续
                if not line.strip():
                    continue
                # ###子标题继续（属于增强块）
                if line.startswith("### "):
                    continue
                # ## 标题结束块
                if line.startswith("## "):
                    break
                # # 标题结束块
                if line.startswith("# "):
                    break
                # 列表项（属于增强块）
                if re.match(r"^\s*[-*]\s", line) or re.match(r"^\s*\d+\.\s", line):
                    continue

                # 其他非空行（非##、非###、非列表），这是原始内容的开始
                # 在这一行前面插入一级标题
                insert_line_offset = sum(1 for l in remaining_lines[:i] if True) + i
                # 计算行号
                start_line = content[:start_search_from].count("\n")
                insert_line = start_line + i + 1
                break

        # 计算插入位置的字符位置
        insert_pos = 0
        for i in range(min(insert_line, len(lines))):
            insert_pos += len(lines[i]) + 1

        h1_line = f"# {title}\n"

        # 检查是否需要在前面添加空行
        if insert_pos > 0 and insert_pos < len(content):
            # 检查前一个字符是否是\n
            if content[insert_pos - 1] == "\n":
                # 前面有换行，检查是否需要额外空行
                if insert_pos > 1 and content[insert_pos - 2] != "\n":
                    # 前面不是双换行，添加一个空行
                    h1_line = f"\n{h1_line}"

        result = content[:insert_pos] + h1_line + content[insert_pos:]
        print(f"  ✅ 在增强内容后生成一级标题: # {title}")
        return result

    except Exception as e:
        print(f"  ⚠️ 生成一级标题失败: {e}")
        import traceback

        traceback.print_exc()
        return content


def clean_duplicate_metadata(content: str) -> str:
    """
    清理 frontmatter 中的重复元数据

    保留有意义的 title（来自 Web Clipper），但删除无意义的 title（如"未命名"）
    这样一级标题 (# 标题) 可以从有意义的 title 生成
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

        title = frontmatter_data.get("title", "")
        title_str = str(title).strip() if title else ""

        # 只删除无意义的 title（空字符串或"未命名"）
        # 保留有意义的 title（来自 Web Clipper）
        if not title_str or title_str == "未命名":
            del frontmatter_data["title"]
            print("  ✅ 已删除无意义的 title 字段")
        else:
            # 保留有意义的 title，使其为frontmatter的第一个字段
            sorted_data = {}
            sorted_data["title"] = frontmatter_data["title"]
            for key, value in frontmatter_data.items():
                if key != "title":
                    sorted_data[key] = value
            frontmatter_data = sorted_data
            print(f"  ✅ 保留了有意义的 title: {title_str}")

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

        return new_content

    except Exception as e:
        print(f"  ⚠️ 清理元数据失败: {e}")
        return content


def identify_frontmatter_type(data: dict) -> str:
    """
    识别 frontmatter 块的类型

    返回值：
    - "obsidian": Obsidian 笔记属性（包含 aliases、up、related、summary 等特定字段）
    - "web_clipper": Web Clipper 元数据（包含 source、author、published 等）
    - "mixed": 混合类型
    """
    # Obsidian 特定字段
    obsidian_fields = {"aliases", "up", "related", "summary", "updated"}
    # Web Clipper 特定字段
    web_clipper_fields = {"source", "author", "published", "description"}

    data_keys = set(data.keys())
    has_obsidian_fields = bool(data_keys & obsidian_fields)
    has_web_clipper_fields = bool(data_keys & web_clipper_fields)

    if has_obsidian_fields and not has_web_clipper_fields:
        return "obsidian"
    elif has_web_clipper_fields and not has_obsidian_fields:
        return "web_clipper"
    elif has_obsidian_fields and has_web_clipper_fields:
        return "mixed"
    else:
        # 都没有特定字段，尝试根据 title 判断
        title = str(data.get("title", "")).strip()
        if title == "未命名" or title == "":
            return "obsidian"
        else:
            return "web_clipper"


def remove_duplicate_frontmatter(content: str) -> str:
    """
    合并多个 frontmatter 块为一个

    某些笔记（如 Web Clipper 导出）可能包含多个 frontmatter 块。
    此函数会智能识别块的类型并正确合并，确保笔记属性留在顶部。
    """
    lines = content.split("\n")

    # 找到所有 frontmatter 块的位置
    frontmatter_blocks = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == "---":
            # 找到一个开始标记
            start = i
            i += 1
            # 找到结束标记
            while i < len(lines) and lines[i].strip() != "---":
                i += 1
            if i < len(lines):
                # 找到了结束标记
                end = i
                frontmatter_blocks.append((start, end))
                i += 1
            else:
                break
        else:
            i += 1

    if len(frontmatter_blocks) <= 1:
        # 没有重复的 frontmatter，直接返回
        return content

    # 有多个 frontmatter 块，需要合并
    print(f"  ℹ️ 检测到 {len(frontmatter_blocks)} 个 frontmatter 块，分析类型...")

    # 解析所有 frontmatter 块并识别类型
    frontmatter_info = []
    for block_idx, (start, end) in enumerate(frontmatter_blocks):
        frontmatter_text = "\n".join(lines[start + 1 : end])
        try:
            data = yaml.safe_load(frontmatter_text)
            if isinstance(data, dict):
                block_type = identify_frontmatter_type(data)
                frontmatter_info.append(
                    {
                        "index": block_idx,
                        "start": start,
                        "end": end,
                        "type": block_type,
                        "data": data,
                    }
                )
                print(f"    块 {block_idx + 1}: {block_type}")
            else:
                frontmatter_info.append(
                    {
                        "index": block_idx,
                        "start": start,
                        "end": end,
                        "type": "invalid",
                        "data": {},
                    }
                )
        except yaml.YAMLError as e:
            print(f"    ⚠️ 块 {block_idx + 1} 解析失败: {str(e)[:30]}...")
            frontmatter_info.append(
                {
                    "index": block_idx,
                    "start": start,
                    "end": end,
                    "type": "invalid",
                    "data": {},
                }
            )

    # 找到 obsidian 块和 web_clipper 块
    obsidian_block = None
    web_clipper_blocks = []
    for info in frontmatter_info:
        block_type = info["type"]

        # 优先规则：如果块包含 Obsidian 特定字段且出现在前面，就作为 obsidian 块
        # 即使它同时包含 Web Clipper 字段（这些字段可能为空）
        if block_type == "obsidian":
            if obsidian_block is None:
                obsidian_block = info
            else:
                web_clipper_blocks.append(info)
        elif block_type == "mixed":
            # mixed 类型的块，检查是否是第一个块（应该保留）
            if obsidian_block is None:
                # 第一个 mixed 块作为 obsidian 块，后续的作为 web_clipper 块
                obsidian_block = info
            else:
                web_clipper_blocks.append(info)
        elif block_type == "web_clipper":
            web_clipper_blocks.append(info)

    # 如果没找到任何块，使用第一个块
    if obsidian_block is None and frontmatter_info:
        obsidian_block = frontmatter_info[0]
        web_clipper_blocks = frontmatter_info[1:]

    if obsidian_block is None:
        return content

    # 合并所有数据到 obsidian 块
    merged_data = dict(obsidian_block["data"])

    for clipper_block in web_clipper_blocks:
        for key, value in clipper_block["data"].items():
            if key not in merged_data:
                merged_data[key] = value
            elif key == "title":
                existing_title = str(merged_data.get(key, "")).strip()
                new_title = str(value).strip() if value else ""
                # 只要 obsidian 的 title 是空或“未命名”，就用 Web Clipper 的 title 覆盖
                if not existing_title or existing_title == "未命名":
                    if new_title and new_title != "未命名":
                        merged_data[key] = value
            elif key == "tags":
                # 合并去重，保留顺序
                tags1 = merged_data.get("tags", [])
                tags2 = value or []
                if not isinstance(tags1, list):
                    tags1 = [tags1] if tags1 else []
                if not isinstance(tags2, list):
                    tags2 = [tags2] if tags2 else []
                merged_tags = []
                seen = set()
                for tag in tags1 + tags2:
                    tag_str = str(tag).strip()
                    if tag_str and tag_str not in seen:
                        merged_tags.append(tag_str)
                        seen.add(tag_str)
                merged_data["tags"] = merged_tags
            else:
                existing_value = merged_data.get(key, "")
                # 判断 obsidian 的值是否为空（空字符串、空列表、None）
                is_empty = (
                    existing_value == ""
                    or existing_value is None
                    or (isinstance(existing_value, list) and len(existing_value) == 0)
                )
                # 只要 obsidian 的值为空，就用 Web Clipper 的值覆盖
                if is_empty and value not in (None, "", []):
                    merged_data[key] = value
                # 否则保留 obsidian 的原值

    # 重新生成 frontmatter
    new_frontmatter_text = yaml.dump(
        merged_data,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    ).rstrip()

    # 构建新内容：保留 obsidian 块的位置，删除其他所有 frontmatter 块
    obsidian_start, obsidian_end = obsidian_block["start"], obsidian_block["end"]

    # 将所有其他 frontmatter 块的行号集合（用于快速查找和跳过）
    other_frontmatter_lines = set()
    for info in frontmatter_info:
        if info != obsidian_block:
            for line_idx in range(info["start"], info["end"] + 1):
                other_frontmatter_lines.add(line_idx)

    # 删除所有其他 frontmatter 块
    result_lines = []
    result_lines.extend(lines[:obsidian_start])  # obsidian 块之前的内容
    result_lines.append("---")
    result_lines.extend(new_frontmatter_text.split("\n"))
    result_lines.append("---")

    # 从 obsidian 块之后开始添加内容，跳过其他 frontmatter 块的所有行
    for i in range(obsidian_end + 1, len(lines)):
        if i not in other_frontmatter_lines:
            result_lines.append(lines[i])

    result = "\n".join(result_lines)

    duplicate_count = len(frontmatter_blocks) - 1
    print(f"  ✅ 已合并 {duplicate_count} 个 frontmatter 块到笔记属性中")
    if "tags" in merged_data:
        tags_str = (
            ", ".join(merged_data["tags"])
            if isinstance(merged_data["tags"], list)
            else str(merged_data["tags"])
        )
        print(f"    📌 保留了 tags 属性: [{tags_str}]")

    # 显示合并后的属性
    print(f"    📋 合并后的属性: {', '.join(sorted(merged_data.keys()))}")

    return result


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

    # 删除重复的 frontmatter，只保留顶部的第一个
    print("\n🧹 删除重复的 frontmatter...")
    content = remove_duplicate_frontmatter(content)

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

    # 调用 enhance_content.py 进行内容增强（先生成增强内容）
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

    # 处理 Web Clipper 元数据：确保有一级标题（放在最后，在所有增强内容之后）
    print("\n📝 处理 Web Clipper 元数据...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = ensure_h1_title_after_enhancements(content)

    # 写回文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

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
