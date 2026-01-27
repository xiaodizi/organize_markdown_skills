---
name: markdown-organizer
description: Organize and beautify markdown files from web pages: download images to local img folder, update image references, and format markdown. Use when user says "@filepath" or "beautify document" or mentions processing markdown with images.
---

# Markdown Organizer

## Overview

Organize and beautify markdown files copied from web pages, automatically download images to local and update references.

## Workflow

### 1. Identify Trigger Conditions

This skill triggers when user meets any of the following conditions:
- Uses `@` symbol to specify local markdown file path
- Says "help me beautify document" or similar request
- Mentions processing markdown files containing images

### 2. Execute Script

Run `{skill_dir}/scripts/organize_markdown.py` to process the file:

```bash
python3 {skill_dir}/scripts/organize_markdown.py /path/to/file.md [base_url]
```

Where `{skill_dir}` is the absolute path to the skill directory.

**Parameter Description:**
- `file.md`: markdown file path (required)
- `base_url`: Original article page URL (optional, for handling relative path images)

### 3. Script Features

The script automatically performs the following operations:

1. **Create img folder**: Create `img` folder in the same directory as the markdown file (if it doesn't exist)

2. **Extract image URLs**: Scan the markdown file and extract all image references `![alt](url)`

3. **Download images**:
   - Download images to `img` folder
   - Use MD5 hash of URL as filename (avoid long filenames or illegal characters)
   - Preserve original image extension
   - Skip download if file already exists

4. **Update image references**: Update image references in markdown to local paths `![alt](./img/filename.jpg)`

5. **Beautify markdown format**:
   - Add blank lines before and after headings
   - Unify list markers to `- `
   - Normalize code blocks
   - Remove excess blank lines
   - Remove trailing whitespace

## Script Location

```
scripts/organize_markdown.py
```

## Examples

### Example 1: Basic Usage

User says:
```
@/Users/user/articles/python-tutorial.md help me beautify document
```

Execute:
```bash
python3 scripts/organize_markdown.py /Users/user/articles/python-tutorial.md
```

### Example 2: Specify Source URL

User says:
```
@article.md beautify this document, original page is https://example.com/post/123
```

Execute:
```bash
python3 scripts/organize_markdown.py article.md https://example.com/post/123
```

## Dependencies

The script requires the following Python packages:
- `requests`: for downloading images

## Quick Start

```bash
# Basic usage
python3 {skill_dir}/scripts/organize_markdown.py your-file.md

# With base URL for relative images
python3 {skill_dir}/scripts/organize_markdown.py your-file.md https://example.com/page
```