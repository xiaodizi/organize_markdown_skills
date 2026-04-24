#!/usr/bin/env python3
"""
修复 Mermaid 代码块中的非法节点内容（如 xxx() → xxx）
用法：python fix_mermaid_nodes.py <.mmd文件路径>
"""
import re
import sys
from pathlib import Path


def fix_nodes(mmd_path: str):
    mmd_path = Path(mmd_path)
    with open(mmd_path, "r", encoding="utf-8") as f:
        content = f.read()
    # 替换所有 xxx()、xxx[]、xxx{{}}、xxx{{}}、xxx<> 为 xxx
    content = re.sub(r"([a-zA-Z0-9_]+)\(\)", r"\1", content)
    content = re.sub(r"([a-zA-Z0-9_]+)\[\]", r"\1", content)
    content = re.sub(r"([a-zA-Z0-9_]+)\{\}", r"\1", content)
    content = re.sub(r"([a-zA-Z0-9_]+)\<\>", r"\1", content)
    # 也可根据需要扩展更多非法写法
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"已修复非法节点内容: {mmd_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python fix_mermaid_nodes.py <.mmd文件路径>")
        sys.exit(1)
    fix_nodes(sys.argv[1])
