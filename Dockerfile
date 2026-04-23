FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl git vim ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# pip 安装 Python 依赖（所有国内脚本需要的包）
RUN pip install --no-cache-dir \
    pyyaml requests beautifulsoup4 html2text

# 设置默认命令
CMD ["bash"]
