# organize

直接执行 markdown 美化脚本，无需思考。

## 执行

```bash
# 获取文件路径并直接运行
FILE_PATH="$1"
BASE_URL="$2"

# 确保依赖已安装
pip install requests -q

# 执行脚本
python3 ~/.gemini/skills/markdown-organizer/scripts/organize_markdown.py "$FILE_PATH" "$BASE_URL"
```
