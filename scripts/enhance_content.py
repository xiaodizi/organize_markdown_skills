#!/usr/bin/env python3
"""
Markdown 内容增强辅助工具

功能：
1. 分析文档结构，识别标题层级、代码块、技术术语
2. 生成内容增强建议
3. 帮助 AI Agent 进行内容优化
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def analyze_document(file_path: str | Path) -> Dict:
    """分析文档结构，返回分析结果"""
    if isinstance(file_path, str):
        file_path = Path(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    analysis = {
        "title": "",
        "headings": [],
        "code_blocks": [],
        "tech_terms": [],
        "steps": [],
        "has_faq": False,
        "has_learning_objectives": False,
        "has_prerequisites": False,
        "suggestions": [],
    }

    # 提取标题（第一个 # 标题）
    for line in lines:
        if line.startswith("# "):
            analysis["title"] = line[2:].strip()
            break

    # 提取所有标题层级
    for i, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            heading = match.group(2).strip()
            analysis["headings"].append(
                {"level": level, "text": heading, "line": i + 1}
            )

    # 提取代码块
    in_code_block = False
    code_block_start = None
    for i, line in enumerate(lines):
        if line.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_block_start = i
                lang = line[3:].strip() if len(line) > 3 else ""
                analysis["code_blocks"].append(
                    {"start_line": i, "language": lang, "content": []}
                )
            else:
                in_code_block = False
                analysis["code_blocks"][-1]["end_line"] = i
                analysis["code_blocks"][-1]["content"] = lines[code_block_start : i + 1]
        elif in_code_block:
            analysis["code_blocks"][-1]["content"].append(line)

    # 检测已有结构
    for heading in analysis["headings"]:
        text_lower = heading["text"].lower()
        if "学习目标" in text_lower or "学习目标" in text_lower:
            analysis["has_learning_objectives"] = True
        if "前置知识" in text_lower or " prerequisites" in text_lower:
            analysis["has_prerequisites"] = True
        if "常见问题" in text_lower or "faq" in text_lower:
            analysis["has_faq"] = True

    # 检测步骤模式
    step_pattern = r"^\d+[.)]\s+|^步骤\s*\d+|^第\s*\d+\s*步"
    for i, line in enumerate(lines):
        if re.search(step_pattern, line, re.IGNORECASE):
            analysis["steps"].append({"line": i + 1, "text": line.strip()})

    # 生成增强建议
    if not analysis["has_learning_objectives"]:
        analysis["suggestions"].append(
            {
                "type": "missing_section",
                "section": "学习目标",
                "description": "文档缺少学习目标部分，建议在开头添加",
            }
        )

    if not analysis["has_prerequisites"]:
        analysis["suggestions"].append(
            {
                "type": "missing_section",
                "section": "前置知识",
                "description": "文档缺少前置知识说明，建议在开头添加",
            }
        )

    if len(analysis["steps"]) > 0 and not analysis["has_faq"]:
        analysis["suggestions"].append(
            {
                "type": "missing_section",
                "section": "常见问题",
                "description": "文档包含步骤说明，建议添加 FAQ 部分解答常见问题",
            }
        )

    if len(analysis["code_blocks"]) > 0:
        for i, cb in enumerate(analysis["code_blocks"]):
            if not cb["language"]:
                analysis["suggestions"].append(
                    {
                        "type": "code_block",
                        "block_index": i,
                        "description": "代码块缺少语言标记，建议添加（如 ```python, ```bash 等）",
                    }
                )

    return analysis


def generate_enhanced_content(file_path: str | Path) -> str:
    """生成增强后的文档内容建议"""
    analysis = analyze_document(file_path)

    suggestions = []
    suggestions.append(f"# 内容增强分析报告: {Path(file_path).name}")
    suggestions.append(f"\n## 文档基本信息")
    suggestions.append(f"- 标题: {analysis['title'] or '未检测到标题'}")
    suggestions.append(f"- 标题层级数: {len(analysis['headings'])}")
    suggestions.append(f"- 代码块数: {len(analysis['code_blocks'])}")
    suggestions.append(f"- 步骤数: {len(analysis['steps'])}")

    suggestions.append(f"\n## 结构检查")
    suggestions.append(
        f"- 学习目标: {'✓ 已存在' if analysis['has_learning_objectives'] else '✗ 缺失'}"
    )
    suggestions.append(
        f"- 前置知识: {'✓ 已存在' if analysis['has_prerequisites'] else '✗ 缺失'}"
    )
    suggestions.append(f"- FAQ: {'✓ 已存在' if analysis['has_faq'] else '✗ 缺失'}")

    suggestions.append(f"\n## 增强建议")
    for i, suggestion in enumerate(analysis["suggestions"], 1):
        suggestions.append(f"\n{i}. [{suggestion['type']}] {suggestion['section']}")
        suggestions.append(f"   {suggestion['description']}")

    suggestions.append(f"\n## 标题结构")
    for heading in analysis["headings"][:10]:  # 只显示前10个
        indent = "  " * (heading["level"] - 1)
        suggestions.append(f"{indent}- {'#' * heading['level']} {heading['text']}")

    if len(analysis["headings"]) > 10:
        suggestions.append(f"... 及其他 {len(analysis['headings']) - 10} 个标题")

    return "\n".join(suggestions)


def enhance_markdown_content(file_path: str | Path) -> str:
    """增强 markdown 内容（在原内容基础上添加缺失部分）"""
    if isinstance(file_path, str):
        file_path = Path(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    analysis = analyze_document(file_path)
    enhanced_content = content

    # 找到第一个标题的位置（用于插入学习目标和前置知识）
    first_heading_match = re.search(r"^#{1,6}\s+.+$", content, re.MULTILINE)

    if first_heading_match:
        heading_pos = first_heading_match.start()

        # 如果缺少学习目标，在标题后添加
        if not analysis["has_learning_objectives"]:
            learning_section = """

## 学习目标

- 理解本文档的核心概念和关键技术
- 掌握相关操作步骤和最佳实践
- 能够独立完成文档中描述的任务
"""
            enhanced_content = (
                enhanced_content[:heading_pos]
                + learning_section
                + enhanced_content[heading_pos:]
            )
            heading_pos += len(learning_section)

        # 如果缺少前置知识，添加前置知识部分
        if not analysis["has_prerequisites"]:
            prerequisites_section = """

## 前置知识

本文档假设您具备以下基础知识：

- 基本的 Markdown 语法
- 相关领域的基础概念
- 能够使用命令行工具

如需补充学习，请参考相关入门教程。
"""
            enhanced_content = (
                enhanced_content[:heading_pos]
                + prerequisites_section
                + enhanced_content[heading_pos:]
            )

    # 如果有步骤但没有 FAQ，在末尾添加 FAQ
    if len(analysis["steps"]) > 0 and not analysis["has_faq"]:
        faq_section = """

## 常见问题

### 如何开始使用？

请按照文档中的步骤顺序进行操作。如有疑问，可参考每节中的详细说明。

### 遇到错误怎么办？

1. 检查步骤是否正确执行
2. 确认环境配置是否正确
3. 查看错误信息并搜索解决方案

### 如何获取更多帮助？

- 参考相关官方文档
- 在社区中提问
- 查看示例代码

"""
        enhanced_content += faq_section

    return enhanced_content


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  分析文档结构:")
        print("    python enhance_content.py --analyze <markdown文件路径>")
        print("  生成增强建议:")
        print("    python enhance_content.py --suggest <markdown文件路径>")
        print("  自动增强内容:")
        print("    python enhance_content.py --enhance <markdown文件路径>")
        sys.exit(1)

    command = sys.argv[1]
    file_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not file_path:
        print("错误: 请指定 markdown 文件路径")
        sys.exit(1)

    if command == "--analyze":
        analysis = analyze_document(file_path)
        print(f"文档分析结果: {file_path}")
        print(f"- 标题: {analysis['title']}")
        print(f"- 标题层级数: {len(analysis['headings'])}")
        print(f"- 代码块数: {len(analysis['code_blocks'])}")
        print(f"- 步骤数: {len(analysis['steps'])}")
        print(f"- 增强建议数: {len(analysis['suggestions'])}")

    elif command == "--suggest":
        suggestions = generate_enhanced_content(file_path)
        print(suggestions)

    elif command == "--enhance":
        enhanced = enhance_markdown_content(file_path)

        # 写入增强后的内容
        output_path = Path(file_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(enhanced)

        print(f"✅ 内容增强完成: {output_path}")

    else:
        print(f"未知命令: {command}")
        print("支持的命令: --analyze, --suggest, --enhance")
        sys.exit(1)


if __name__ == "__main__":
    main()
