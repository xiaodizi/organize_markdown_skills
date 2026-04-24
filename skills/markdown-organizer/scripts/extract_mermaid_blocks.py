#!/usr/bin/env python3
"""
提取 markdown 文件中的所有 mermaid 代码块，保存为单独的 .mmd 文件
用法：python extract_mermaid_blocks.py <markdown文件路径>
"""
import re
import sys
from pathlib import Path


def extract_mermaid_blocks(md_path: str):
    md_path = Path(md_path)
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    # 匹配 mermaid 代码块
    pattern = re.compile(r"```mermaid\s*([\s\S]*?)```", re.MULTILINE)
    matches = pattern.findall(content)
    out_files = []
    for idx, block in enumerate(matches):
        out_file = md_path.parent / f"mermaid_block_{idx+1}.mmd"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(block.strip() + "\n")
        out_files.append(str(out_file))
    print(f"提取到 {len(out_files)} 个 mermaid 代码块: {out_files}")
    return out_files


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python extract_mermaid_blocks.py <markdown文件路径>")
        sys.exit(1)
    extract_mermaid_blocks(sys.argv[1])
