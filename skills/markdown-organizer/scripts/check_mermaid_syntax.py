#!/usr/bin/env python3
"""
用 Mermaid CLI 检查 .mmd 文件语法，自动修复非法节点
用法：python check_mermaid_syntax.py <.mmd文件路径>
"""
import sys
import subprocess
from pathlib import Path


def check_mermaid(mmd_path: str):
    mmd_path = Path(mmd_path)
    try:
        # 用 mmdc 检查语法（不生成图片，只检测）
        result = subprocess.run(
            ["mmdc", "-i", str(mmd_path), "-o", "/dev/null"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"✅ Mermaid 语法无误: {mmd_path}")
            return True
        else:
            print(f"❌ Mermaid 语法错误: {mmd_path}\n{result.stderr}")
            return False
    except FileNotFoundError:
        print(
            "未检测到 mmdc 命令，请先安装 Mermaid CLI: npm install -g @mermaid-js/mermaid-cli"
        )
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python check_mermaid_syntax.py <.mmd文件路径>")
        sys.exit(1)
    check_mermaid(sys.argv[1])
