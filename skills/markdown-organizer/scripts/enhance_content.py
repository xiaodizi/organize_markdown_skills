#!/usr/bin/env python3
"""
Markdown 文档增强工具

功能：
1. 分析文档结构和内容
2. 基于文档内容自动生成简洁的摘要
3. 将摘要插入到文档顶部（frontmatter之后）
"""

import re
import sys
from pathlib import Path
from typing import Dict, List


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
        "paragraphs": [],
        "code_blocks": [],
        "has_summary": False,
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
            analysis["headings"].append({"level": level, "text": heading, "line": i + 1})

    # 提取段落（首个大标题后、代码块外的文本）
    in_code_block = False
    in_frontmatter = False
    first_heading_found = False

    for i, line in enumerate(lines):
        # 处理frontmatter
        if i == 0 and line.startswith("---"):
            in_frontmatter = True
            continue
        if in_frontmatter and line.startswith("---"):
            in_frontmatter = False
            continue
        if in_frontmatter:
            continue

        # 处理代码块
        if line.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # 检测首个大标题
        if re.match(r"^# ", line):
            first_heading_found = True
            continue

        # 提取首个标题后的段落
        if first_heading_found and line.strip() and not re.match(r"^#+\s", line):
            analysis["paragraphs"].append(line.strip())

    # 检测是否已有摘要
    for heading in analysis["headings"]:
        text_lower = heading["text"].lower()
        if text_lower.strip() == "摘要" or text_lower.strip() == "概述" or text_lower.strip() == "summary":
            analysis["has_summary"] = True
            break

    return analysis


def extract_key_topics(headings: List[Dict], paragraphs: List[str]) -> List[str]:
    """从文档中提取关键话题"""
    topics = []

    # 从二级标题提取主要话题
    for heading in headings:
        if heading["level"] == 2:  # ## 标题
            topic = heading["text"]
            # 去除特殊标题
            if topic.lower() not in ["摘要", "概述", "summary", "介绍"]:
                topics.append(topic)

    return topics[:5]  # 限制到前5个话题


def extract_key_sentences(paragraphs: List[str], limit: int = 2) -> List[str]:
    """从段落中提取关键句子"""
    sentences = []

    for para in paragraphs[:5]:  # 只看前5个段落
        # 分割句子
        para_sentences = re.split(r'[。！？；:：]', para)
        for sent in para_sentences:
            sent = sent.strip()
            if len(sent) > 10:  # 至少10个字符
                sentences.append(sent)
                if len(sentences) >= limit:
                    return sentences

    return sentences


def generate_summary(title: str, headings: List[Dict], paragraphs: List[str]) -> str:
    """基于文档内容生成摘要"""
    lines = []
    lines.append("## 摘要")
    lines.append("")

    # 生成摘要内容
    summary_parts = []

    # 1. 主标题作为主题
    if title:
        summary_parts.append(f"本文介绍了 {title} 的相关内容。")

    # 2. 提取关键话题
    topics = extract_key_topics(headings, paragraphs)
    if topics:
        topics_str = "、".join(topics)
        summary_parts.append(f"主要涵盖以下方面：{topics_str}。")

    # 3. 提取关键句子
    key_sentences = extract_key_sentences(paragraphs, limit=1)
    if key_sentences:
        summary_parts.append(f"文档的核心内容：{key_sentences[0]}。")

    # 4. 统计信息
    level2_headings = [h for h in headings if h["level"] == 2]
    if level2_headings:
        summary_parts.append(f"全文共包含 {len(level2_headings)} 个主要章节。")

    # 拼接摘要
    if summary_parts:
        lines.append("".join(summary_parts))
    else:
        lines.append("本文档提供了详细的技术信息和实践指导。")

    lines.append("")
    return "\n".join(lines)


def find_insert_position_below_frontmatter(content: str) -> int | None:
    """返回 frontmatter 结束后的插入位置
    
    优先级：
    1. 如果有一级标题，在一级标题之后
    2. 否则在 frontmatter 之后
    """
    lines = content.split("\n")

    # 文档必须以 --- 开头
    if not lines or lines[0].strip() != "---":
        return None

    # 查找 frontmatter 结束标记 ---
    frontmatter_end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            frontmatter_end = i
            break
    
    if frontmatter_end is None:
        return None
    
    # 检查 frontmatter 之后是否有一级标题
    for i in range(frontmatter_end + 1, len(lines)):
        if lines[i].startswith("# ") and not lines[i].startswith("## "):
            # 找到一级标题，在它之后插入
            # 计算位置
            position = 0
            for j in range(i + 1):
                position += len(lines[j]) + 1  # +1 for newline character
            return position
    
    # 没有找到一级标题，在 frontmatter 后插入
    position = 0
    for j in range(frontmatter_end + 1):  # 包括结束的 --- 行
        position += len(lines[j]) + 1  # +1 for newline character
    return position


def enhance_markdown_content(file_path: str | Path) -> str:
    """增强 markdown 内容：添加摘要"""
    if isinstance(file_path, str):
        file_path = Path(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    analysis = analyze_document(file_path)

    # 如果已有摘要，直接返回原内容（不做任何修改）
    if analysis["has_summary"]:
        return content

    # 找到插入位置
    insert_pos = find_insert_position_below_frontmatter(content)
    if insert_pos is None:
        # 没有 frontmatter，尝试找第一个标题
        first_heading_match = re.search(r"^# .+$", content, re.MULTILINE)
        if first_heading_match:
            insert_pos = first_heading_match.end() + 1
        else:
            # 没有标题也没有 frontmatter，插入到最前面
            insert_pos = 0
    else:
        # 如果find_insert_position_below_frontmatter返回的位置，再次检查是否真的在一级标题之后
        # 这是为了处理一些edge case
        # 获取当前位置后的内容
        content_after_pos = content[insert_pos:]
        # 检查是否紧接着是一级标题
        if not content_after_pos.lstrip().startswith("# "):
            # 没有一级标题紧跟着，尝试找下一个一级标题
            h1_match = re.search(r"^# .+$", content_after_pos, re.MULTILINE)
            if h1_match:
                # 找到了一级标题，调整插入位置到该标题之后
                insert_pos = insert_pos + h1_match.end() + 1

    # 生成摘要
    summary = generate_summary(analysis["title"], analysis["headings"], analysis["paragraphs"])

    # 插入摘要（保持前面的 frontmatter 完整）
    enhanced_content = (
        content[:insert_pos] + "\n" + summary + "\n" + content[insert_pos:]
    )

    # 规范标题前空行
    enhanced_content = re.sub(r"([^\n])\n(#{1,6}\s)", r"\1\n\n\2", enhanced_content)

    # 确保文件以换行结束
    enhanced_content = enhanced_content.rstrip("\n") + "\n"

    return enhanced_content


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  分析文档结构:")
        print("    python enhance_content.py --analyze <markdown文件路径>")
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
        print(f"- 段落数: {len(analysis['paragraphs'])}")
        print(f"- 已有摘要: {'是' if analysis['has_summary'] else '否'}")

    elif command == "--enhance":
        enhanced = enhance_markdown_content(file_path)

        # 写入增强后的内容（保持所有原有内容，包括 frontmatter）
        output_path = Path(file_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(enhanced)

        print(f"✅ 内容增强完成: {output_path}")

    else:
        print(f"未知命令: {command}")
        print("支持的命令: --analyze, --enhance")
        sys.exit(1)


if __name__ == "__main__":
    main()
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
    "markdown": ["Markdown", "markdown"],
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

STOP_WORDS = {
    "如何",
    "怎么",
    "什么",
    "教程",
    "指南",
    "入门",
    "学习",
    "使用",
    "实战",
    "完整",
    "详细",
    "快速",
    "方案",
    "方法",
    "详解",
    "介绍",
    "文档",
    "示例",
    "example",
    "guide",
    "tutorial",
    "learn",
    "with",
    "from",
    "that",
    "this",
}

PREREQUISITE_DESCRIPTIONS = {
    "Python 基础": "了解语法、虚拟环境与 `pip` 常见操作。",
    "JavaScript 基础": "理解变量、函数、模块与异步基础。",
    "TypeScript 基础": "了解类型系统、接口与泛型的基本用法。",
    "JavaScript/TypeScript 基础": "理解 JS 语法与 TS 类型标注，能阅读前端工程代码。",
    "命令行基础": "能在终端完成目录切换、文件操作与命令执行。",
    "Git 版本控制": "了解分支、提交与拉取/推送等基础流程。",
    "Markdown 语法": "熟悉标题、列表、代码块与链接等常见语法。",
    "HTML/CSS 基础": "能理解页面结构与基础样式规则。",
    "数据库基础": "了解基本数据模型与常见查询语句。",
    "API 概念": "理解请求/响应、状态码与接口调用流程。",
    "Docker 基础": "了解镜像、容器与常用运行命令。",
    "编程基础知识": "具备变量、条件、循环与函数等通用编程能力。",
}

PREREQUISITE_PRIORITY = [
    "Python 基础",
    "JavaScript/TypeScript 基础",
    "JavaScript 基础",
    "TypeScript 基础",
    "React 基础",
    "Vue 基础",
    "命令行基础",
    "Git 版本控制",
    "API 概念",
    "数据库基础",
    "Docker 基础",
    "Markdown 语法",
    "HTML/CSS 基础",
    "编程基础知识",
]


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

    # 检测已有结构（精确匹配，避免误检）
    for heading in analysis["headings"]:
        text_lower = heading["text"].lower()
        # 精确匹配标题：不是包含关键词，而是标题本身就是这些名称
        if text_lower.strip() == "学习目标":
            analysis["has_learning_objectives"] = True
        if text_lower.strip() == "前置知识" or text_lower.strip() == "prerequisites":
            analysis["has_prerequisites"] = True
        if text_lower.strip() == "常见问题" or text_lower.strip() == "faq":
            analysis["has_faq"] = True

    # 检测步骤模式
    step_pattern = r"^(?:#{1,6}\s*)?(?:\d+[.)]\s+|步骤\s*\d+|第\s*\d+\s*步)"
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
                elif category == "react":
                    detected_prereqs.add("React 基础")
                elif category == "vue":
                    detected_prereqs.add("Vue 基础")
                elif category == "shell":
                    detected_prereqs.add("命令行基础")
                elif category == "git":
                    detected_prereqs.add("Git 版本控制")
                elif category == "html_css":
                    detected_prereqs.add("HTML/CSS 基础")
                elif category == "sql":
                    detected_prereqs.add("数据库基础")
                elif category == "api":
                    detected_prereqs.add("API 概念")
                elif category == "docker":
                    detected_prereqs.add("Docker 基础")
                elif category == "markdown":
                    detected_prereqs.add("Markdown 语法")
                break

    # 检测是否需要特定深度的基础知识
    if any(
        kw in content for kw in ["教程", "入门", "初学者", "learn", "tutorial", "guide"]
    ):
        detected_prereqs.add("编程基础知识")

    # 去重和去泛化：JS/TS 同时出现时合并；已有多项具体技能时移除泛化项
    if "JavaScript 基础" in detected_prereqs and "TypeScript 基础" in detected_prereqs:
        detected_prereqs.discard("JavaScript 基础")
        detected_prereqs.discard("TypeScript 基础")
        detected_prereqs.add("JavaScript/TypeScript 基础")

    specific_count = len(detected_prereqs - {"编程基础知识"})
    if specific_count >= 3:
        detected_prereqs.discard("编程基础知识")

    return detected_prereqs


def generate_learning_objectives(
    content: str, title: str, headings: List[Dict]
) -> List[str]:
    """根据文档内容生成个性化的学习目标"""
    objectives = []
    content_lower = content.lower()

    def extract_topic_candidates(text: str) -> List[str]:
        candidates = re.findall(
            r"[A-Za-z][A-Za-z0-9+._-]{2,}|[\u4e00-\u9fff]{2,8}", text
        )
        return [
            word
            for word in candidates
            if word.lower() not in STOP_WORDS and word not in STOP_WORDS
        ]

    # 从标题提取关键词（兼容中英文）
    title_keywords = extract_topic_candidates(title)
    main_topic = title_keywords[0] if title_keywords else None

    # 提取文档中的主要章节主题
    topic_words = []
    for heading in headings[:6]:
        topic_words.extend(extract_topic_candidates(heading["text"]))

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
    lines.append("## 前置知识")
    lines.append("")

    if detected_prereqs:
        lines.append("本文档涉及以下技术栈和概念，建议提前了解：")
        lines.append("")
        prioritized = sorted(
            detected_prereqs,
            key=lambda x: (
                PREREQUISITE_PRIORITY.index(x)
                if x in PREREQUISITE_PRIORITY
                else len(PREREQUISITE_PRIORITY)
            ),
        )
        for prereq in prioritized[:6]:
            description = PREREQUISITE_DESCRIPTIONS.get(
                prereq, "建议具备相关基础后再开始实操。"
            )
            lines.append(f"- **{prereq}**：{description}")
    else:
        lines.append("本文档假设您具备以下基础知识：")
        lines.append("")
        lines.append("- 基本的编程思维和逻辑能力")
        lines.append("- 能够阅读和理解技术文档")

    lines.append("")
    lines.append("如遇到不熟悉的概念，建议先补充相关基础知识再继续学习。")
    lines.append("")

    return "\n".join(lines)


def generate_learning_objectives_content(objectives: List[str]) -> str:
    """生成学习目标部分的 Markdown 内容"""
    lines = []
    lines.append("## 学习目标")
    lines.append("")
    lines.append("完成本教程后，您将能够：")
    lines.append("")
    for obj in objectives:
        lines.append(f"- {obj}")
    lines.append("")
    return "\n".join(lines)


def generate_faq_content(content: str, analysis: Dict) -> str:
    """根据文档内容生成 FAQ（避免固定模板）"""
    title = analysis["title"] or "本文内容"

    headings = [
        h["text"]
        for h in analysis["headings"]
        if h["level"] <= 3
        and all(k not in h["text"] for k in ["学习目标", "前置知识", "常见问题", "FAQ"])
    ]
    top_headings = headings[:3]

    detected_prereqs = sorted(detect_prerequisites(content))
    key_terms = extract_key_terms(content)[:3]
    step_count = len(analysis["steps"])

    lines = ["## 常见问题", ""]

    lines.append("### 这篇文档建议按什么顺序学习？")
    if top_headings:
        lines.append("建议按以下顺序阅读并实践：" + " -> ".join(top_headings) + "。")
    else:
        lines.append("建议先通读全文，再按章节中的示例逐步实践。")
    lines.append("")

    lines.append("### 开始实操前需要准备什么？")
    if detected_prereqs:
        lines.append("建议先准备这些基础：" + "、".join(detected_prereqs[:4]) + "。")
    else:
        lines.append("建议具备基础编程能力，并能使用命令行执行示例命令。")
    lines.append("")

    lines.append("### 实操过程中遇到问题怎么排查？")
    if step_count > 0:
        lines.append(
            f"本文包含约 {step_count} 个操作步骤，建议逐步核对输入参数、环境版本和命令执行结果，优先定位首个报错点。"
        )
    else:
        lines.append("建议先复现问题，再结合报错信息定位到对应章节进行排查。")
    lines.append("")

    lines.append(f"### 学完后如何验证自己掌握了《{title}》？")
    if key_terms:
        lines.append(
            "可以尝试脱离文档，独立完成一个最小可运行示例，并正确使用这些关键点："
            + "、".join(key_terms)
            + "。"
        )
    else:
        lines.append("可以尝试独立复现文档中的核心流程，并向他人解释关键步骤和原理。")
    lines.append("")

    return "\n".join(lines)


def find_insert_position_below_frontmatter(content: str) -> int | None:
    """返回 frontmatter 结束后的插入位置（若不存在则返回 None）。"""
    frontmatter_match = re.match(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", content, re.DOTALL)
    if frontmatter_match:
        return frontmatter_match.end()
    return None


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

    # 找到插入位置：优先放在 frontmatter（文档属性）之后，否则放在首个标题前
    insert_pos = find_insert_position_below_frontmatter(content)
    if insert_pos is None:
        first_heading_match = re.search(r"^#{1,6}\s+.+$", content, re.MULTILINE)
        if first_heading_match:
            insert_pos = first_heading_match.start()
        else:
            # 如果没有标题，插入到文档开头
            insert_pos = 0

    prepend_sections = []

    # 如果缺少学习目标，生成个性化内容
    if not analysis["has_learning_objectives"]:
        # 根据文档实际内容生成个性化的学习目标
        learning_objectives = generate_learning_objectives(
            content, analysis["title"], analysis["headings"]
        )
        learning_section = generate_learning_objectives_content(learning_objectives)
        prepend_sections.append(learning_section)

    # 如果缺少前置知识，生成个性化内容
    if not analysis["has_prerequisites"]:
        # 根据文档内容检测需要的前置知识
        detected_prereqs = detect_prerequisites(content)
        prerequisites_section = generate_prerequisites_content(
            content, detected_prereqs
        )
        prepend_sections.append(prerequisites_section)

    # 如果有步骤但没有 FAQ，在顶部添加 FAQ（与学习目标、前置知识一起）
    if len(analysis["steps"]) > 0 and not analysis["has_faq"]:
        faq_section = generate_faq_content(content, analysis)
        prepend_sections.append(faq_section)

    if prepend_sections and insert_pos is not None:
        prepend_block = "\n".join(prepend_sections).rstrip() + "\n\n"
        enhanced_content = (
            enhanced_content[:insert_pos]
            + prepend_block
            + enhanced_content[insert_pos:]
        )

    # 规范标题前空行，避免出现 "...文本。## 标题" 的粘连问题
    enhanced_content = re.sub(r"([^\n])\n(#{1,6}\s)", r"\1\n\n\2", enhanced_content)

    # 确保文件以换行结束，避免标题渲染异常
    enhanced_content = enhanced_content.rstrip("\n") + "\n"

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
