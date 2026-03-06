# url-to-markdown

将网页 URL 转换为 Markdown 文档并保存到本地。

## 执行

```bash
# 获取 URL 并直接运行
URL="$1"
OUTPUT_PATH="$2"

# 确保依赖已安装
pip install requests beautifulsoup4 html2text -q

# 执行脚本
python3 ~/.gemini/skills/url-to-markdown/scripts/url_to_markdown.py "$URL" "$OUTPUT_PATH"
```
