#!/usr/bin/env python3
"""
Markdown 格式规范化工具

功能：规范化标题前空行，确保文件末尾有换行符
"""

import re
import sys
from pathlib import Path


def normalize_markdown(file_path: str | Path) -> str:
    """规范化 markdown 格式"""
    if isinstance(file_path, str):
        file_path = Path(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 规范标题前空行
    content = re.sub(r"([^\n])\n(#{1,6}\s)", r"\1\n\n\2", content)

    # 确保文件以换行结束
    content = content.rstrip("\n") + "\n"

    return content


def main():
    if len(sys.argv) < 3 or sys.argv[1] != "--enhance":
        print("用法: python enhance_content.py --enhance <markdown文件路径>")
        sys.exit(1)

    file_path = Path(sys.argv[2])
    content = normalize_markdown(file_path)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ 格式规范化完成: {file_path}")


if __name__ == "__main__":
    main()
