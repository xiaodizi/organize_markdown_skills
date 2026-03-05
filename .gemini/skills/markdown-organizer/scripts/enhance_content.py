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
from collections import Counter
from pathlib import Path
from typing import Dict, List, Set, Tuple


# 常见技术栈关键词库，用于识别前置知识
TECH_STACK_KEYWORDS = {
    # 编程语言
    "python": ["Python", "python", "pip", "py"],
    "javascript": ["JavaScript", "JS", "javascript", "node", "npm", "yarn", "Node.js"],
    "typescript": ["TypeScript", "typescript", "ts", "TS"],
    "ruby": ["Ruby", "ruby", "gem", "Rails"],
    "go": ["Go", "golang", "Golang"],
    "rust": ["Rust", "rust", "cargo"],
    "java": ["Java", "java", "Maven", "Gradle"],
    "csharp": ["C#", "CSharp", ".NET", "dotnet"],
    "cpp": ["C++", "cpp", "C/C++"],
    "shell": ["bash", "shell", "sh", "zsh", "命令行", "终端", "terminal"],
    # 前端框架
    "react": ["React", "react", "JSX", "Next.js", "Nextjs"],
    "vue": ["Vue", "vue", "Nuxt"],
    "angular": ["Angular", "angular"],
    "html_css": ["HTML", "HTML5", "CSS", "CSS3"],
    "tailwind": ["Tailwind", "tailwind"],
    # 后端框架
    "fastapi": ["FastAPI", "fastapi"],
    "flask": ["Flask", "flask"],
    "django": ["Django", "django"],
    "express": ["Express", "express", "Express.js"],
    "spring": ["Spring", "spring", "Spring Boot"],
    # 数据库
    "sql": ["SQL", "sql", "MySQL", "PostgreSQL", "SQLite"],
    "mongodb": ["MongoDB", "mongodb", "NoSQL"],
    "redis": ["Redis", "redis"],
    # 工具/平台
    "git": ["Git", "git", "GitHub", "gitlab", "Gitee"],
    "docker": ["Docker", "docker", "container"],
    "kubernetes": ["Kubernetes", "k8s", "kubectl"],
    "linux": ["Linux", "linux", "Ubuntu", "CentOS"],
    "aws": ["AWS", "S3", "EC2", "Lambda"],
    # AI/ML
    "llm": ["LLM", "OpenAI", "Claude", "GPT", "大语言模型"],
    "pytorch": ["PyTorch", "pytorch", "torch"],
    "tensorflow": ["TensorFlow", "tensorflow"],
    "ml": ["机器学习", "Machine Learning", "深度学习", "Deep Learning"],
    # 其他常见概念
    "api": ["API", "REST", "RESTful", "接口", "endpoint"],
    "auth": ["Auth", "认证", "授权", "JWT", "OAuth", "登录"],
    "cloud": ["云", "Cloud", "Serverless"],
}

# 常见前置知识要求
PREREQUISITE_TEMPLATES = {
    "编程语言基础": [
        "具备编程基础知识，了解变量、函数、控制流程等概念",
        "能够编写和运行简单的程序",
    ],
    "命令行使用": [
        "熟悉命令行基本操作（Linux/Mac 使用 Terminal，Windows 使用 PowerShell）",
        "了解基本的文件操作命令（cd, ls, mkdir, cp, mv）",
    ],
    "Git版本控制": [
        "了解 Git 基本概念（仓库、提交、分支）",
        "能够执行基本的 Git 操作（clone, add, commit, push, pull）",
    ],
    "Markdown语法": [
        "了解 Markdown 基本语法（标题、列表、代码块、链接）",
        "能够使用 Markdown 编写文档",
    ],
    "HTTP协议": [
        "了解 HTTP 基本概念（请求/响应、状态码、Headers）",
        "理解 RESTful API 的设计原则",
    ],
    "前端基础": [
        "了解 HTML、CSS、JavaScript 基础",
        "能够阅读和修改前端代码",
    ],
    "数据库基础": [
        "了解关系型数据库基本概念（表、行、列、SQL）",
        "能够执行基本的数据库操作",
    ],
    "API调用": [
        "了解 API 调用方式（REST、GraphQL）",
        "能够使用工具（如 curl、Postman）测试 API",
    ],
    "容器化基础": [
        "了解 Docker 基本概念和常用命令",
        "能够构建和运行 Docker 容器",
    ],
    "AI/LLM基础": [
        "了解大语言模型的基本概念和使用方式",
        "具备一定的提示词（Prompt）编写经验",
    ],
}


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


def extract_key_terms(content: str) -> List[str]:
    """从文档内容中提取关键技术术语"""
    # 提取被反引号包裹的代码词汇
    code_terms = re.findall(r"`([^`]+)`", content)

    # 提取大写的英文缩写词（3个字母以上）
    acronyms = re.findall(r"\b([A-Z]{3,})\b", content)

    # 提取常见的函数/方法名模式
    function_patterns = re.findall(r"(\w+)\s*\(", content)
    common_funcs = {
        "print",
        "return",
        "if",
        "else",
        "for",
        "while",
        "def",
        "class",
        "import",
        "from",
        "export",
        "default",
        "const",
        "let",
        "var",
        "function",
    }
    functions = [
        f for f in function_patterns if f.lower() not in common_funcs and len(f) > 2
    ]

    # 合并并去重
    all_terms = list(set(code_terms + acronyms + functions))
    return all_terms[:15]  # 限制返回数量


def detect_prerequisites(content: str) -> Set[str]:
    """根据文档内容检测相关的前置知识要求"""
    content_lower = content.lower()
    detected_prereqs = set()

    for category, keywords in TECH_STACK_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in content_lower:
                if category == "python":
                    detected_prereqs.add("Python 基础")
                elif category == "javascript":
                    detected_prereqs.add("JavaScript 基础")
                elif category == "typescript":
                    detected_prereqs.add("TypeScript 基础")
                elif category == "shell":
                    detected_prereqs.add("命令行基础")
                elif category == "git":
                    detected_prereqs.add("Git 版本控制")
                elif category == "Markdown语法":
                    detected_prereqs.add("Markdown 语法")
                elif category == "html_css":
                    detected_prereqs.add("HTML/CSS 基础")
                elif category == "sql":
                    detected_prereqs.add("数据库基础")
                elif category == "api":
                    detected_prereqs.add("API 概念")
                elif category == "docker":
                    detected_prereqs.add("Docker 基础")
                break

    # 检测是否需要特定深度的基础知识
    if any(
        kw in content for kw in ["教程", "入门", "初学者", "learn", "tutorial", "guide"]
    ):
        detected_prereqs.add("编程基础知识")

    return detected_prereqs


def generate_learning_objectives(
    content: str, title: str, headings: List[Dict]
) -> List[str]:
    """根据文档内容生成个性化的学习目标"""
    objectives = []
    content_lower = content.lower()

    # 从标题提取关键词
    title_keywords = re.findall(r"\b\w+\b", title.lower())
    main_topic = next(
        (
            w
            for w in title_keywords
            if len(w) > 3
            and w not in ["如何", "怎么", "什么", "教程", "指南", "入门", "学习"]
        ),
        None,
    )

    # 提取文档中的主要章节主题
    topic_words = []
    for heading in headings[:5]:
        words = re.findall(r"\b\w+\b", heading["text"].lower())
        topic_words.extend([w for w in words if len(w) > 3])

    # 统计高频主题词
    topic_counter = Counter(topic_words)
    main_topics = [word for word, _ in topic_counter.most_common(3)]

    # 检测文档类型
    is_tutorial = any(
        kw in content
        for kw in ["步骤", "步骤一", "第一步", "1.", "2.", "3.", "首先", "然后"]
    )
    is_concept = any(
        kw in content for kw in ["概念", "原理", "介绍", "什么是", "概念介绍"]
    )
    is_reference = any(
        kw in content for kw in ["API", "接口", "参数", "属性", "方法", "函数", "配置"]
    )
    is_troubleshooting = any(
        kw in content for kw in ["错误", "问题", "解决", "debug", "排查", "修复"]
    )

    # 生成个性化学习目标
    if main_topic:
        objectives.append(f"理解 {main_topic} 的核心概念和工作原理")

    if main_topics:
        for topic in main_topics[:2]:
            if topic != main_topic:
                objectives.append(f"掌握 {topic} 的使用方法和使用场景")

    objectives.append("理解文档中涉及的关键术语和技术概念")

    if is_tutorial:
        objectives.append("能够按照步骤独立完成实际操作")
        objectives.append("掌握常见问题的排查和解决方法")
    elif is_concept:
        objectives.append("能够清晰解释相关概念和原理")
    elif is_reference:
        objectives.append("能够查阅文档快速找到所需的 API 和配置说明")
    elif is_troubleshooting:
        objectives.append("能够识别和解决常见错误")
        objectives.append("掌握调试技巧和排查思路")

    objectives.append("能够将所学知识应用到实际项目中")

    return objectives[:6]  # 限制数量


def generate_prerequisites_content(content: str, detected_prereqs: Set[str]) -> str:
    """生成个性化的前置知识内容"""
    lines = []
    lines.append("\n## 前置知识")
    lines.append("")

    if detected_prereqs:
        lines.append("本文档涉及以下技术栈和概念，建议提前了解：")
        lines.append("")
        for prereq in sorted(detected_prereqs):
            lines.append(f"- **{prereq}**")
    else:
        lines.append("本文档假设您具备以下基础知识：")
        lines.append("")
        lines.append("- 基本的编程思维和逻辑能力")
        lines.append("- 能够阅读和理解技术文档")

    lines.append("")
    lines.append("如遇到不熟悉的概念，建议先补充相关基础知识再继续学习。")

    return "\n".join(lines)


def generate_learning_objectives_content(objectives: List[str]) -> str:
    """生成学习目标部分的 Markdown 内容"""
    lines = []
    lines.append("\n## 学习目标")
    lines.append("")
    lines.append("完成本教程后，您将能够：")
    lines.append("")
    for obj in objectives:
        lines.append(f"- {obj}")
    return "\n".join(lines)


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
        section = suggestion.get("section", suggestion.get("type", "建议"))
        suggestions.append(f"\n{i}. [{suggestion['type']}] {section}")
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

        # 如果缺少学习目标，生成个性化内容
        if not analysis["has_learning_objectives"]:
            # 根据文档实际内容生成个性化的学习目标
            learning_objectives = generate_learning_objectives(
                content, analysis["title"], analysis["headings"]
            )
            learning_section = generate_learning_objectives_content(learning_objectives)

            enhanced_content = (
                enhanced_content[:heading_pos]
                + learning_section
                + enhanced_content[heading_pos:]
            )
            heading_pos += len(learning_section)

        # 如果缺少前置知识，生成个性化内容
        if not analysis["has_prerequisites"]:
            # 根据文档内容检测需要的前置知识
            detected_prereqs = detect_prerequisites(content)
            prerequisites_section = generate_prerequisites_content(
                content, detected_prereqs
            )

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
