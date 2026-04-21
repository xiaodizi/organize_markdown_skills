# Frontmatter 合并修复说明

## 问题描述

当处理包含多个 YAML frontmatter 块的 markdown 文件时（特别是 Web Clipper 导出的文件），第二个及后续的 frontmatter 块没有被正确合并到第一个 frontmatter 块中，导致文件中仍然存在多个 frontmatter 块。

**错误案例**：
```markdown
---
title: "Original Title"
created: 2026-04-20
---

内容...

---
title: "AI Knowledge Layer"
source: "https://..."
author: [...]
published: 2026-04-14
tags:
  - "clippings"
---
```

处理后仍然是两个 frontmatter 块，没有合并。

## 根本原因

在 `organize_markdown.py` 的 `remove_duplicate_frontmatter()` 函数中，跳过其他 frontmatter 块的逻辑存在缺陷：

```python
# 原有的有问题的逻辑
while i < len(lines):
    if lines[i].strip() == "---":
        skip_this = False
        for other_start, other_end in frontmatter_blocks[1:]:
            if i == other_start:  # ❌ 这个检查不可靠
                i = other_end + 1
                skip_this = True
                break
```

当遍历文件行时，对 `i == other_start` 的检查容易因为循环逻辑而遗漏某些 frontmatter 块。

## 修复方案

使用集合（set）来预计算所有需要跳过的行号，而不是在循环中逐一匹配：

```python
# 新的改进逻辑
# 将所有其他 frontmatter 块的行号集合（用于快速查找和跳过）
other_frontmatter_lines = set()
for other_start, other_end in frontmatter_blocks[1:]:
    for line_idx in range(other_start, other_end + 1):
        other_frontmatter_lines.add(line_idx)

# 简单地检查行是否需要跳过
for i in range(first_end + 1, len(lines)):
    if i not in other_frontmatter_lines:
        result_lines.append(lines[i])
```

## 改进效果

### ✅ 修复后的行为

- **正确合并**：所有 frontmatter 块的属性都被正确合并到第一个块中
- **保留所有属性**：包括 title、source、author、published、tags 等所有属性
- **合并列表属性**：当属性是列表类型时（如 tags、author），会进行去重合并
- **清晰的日志**：新增显示合并后的属性列表

### 修复后的输出示例

```
  ℹ️ 检测到 2 个 frontmatter 块，尝试合并...
  ✅ 已合并 1 个 frontmatter 块
    📌 保留了 tags 属性: [clippings]
    📋 合并后的属性: author, created, description, published, source, tags, title
```

## 技术细节

### 改进点

1. **性能优化**：从 O(n*m) 复杂度（n = 总行数，m = frontmatter 块数）优化为 O(n + m)
2. **逻辑简化**：减少嵌套循环，降低出错可能性
3. **更好的可观测性**：添加合并属性列表日志，便于调试

### 兼容性

- ✅ 支持任意数量的 frontmatter 块（2个、3个、更多）
- ✅ 支持所有 YAML 数据类型（字符串、列表、对象等）
- ✅ 保持与现有处理流程的兼容性

## 验证方式

测试命令：
```bash
python3 skills/markdown-organizer/scripts/organize_markdown.py test_file.md
```

验证文件中只有一个 frontmatter 块，且包含所有合并的属性。

## 文件修改

- **修改文件**：`skills/markdown-organizer/scripts/organize_markdown.py`
- **修改函数**：`remove_duplicate_frontmatter()`
- **修改行数**：约 40-50 行（第 270-350 行）
