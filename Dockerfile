FROM python:3.11-slim

WORKDIR /app

# 配置代理 - 访问宿主机的代理
ENV http_proxy=http://host.docker.internal:7890
ENV https_proxy=http://host.docker.internal:7890
ENV NO_PROXY=localhost,127.0.0.1,.local,host.docker.internal

# 使用国内镜像源（加速）- 检查 sources.list 是否存在
RUN if [ -f /etc/apt/sources.list ]; then \
    sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list; \
fi

# 安装系统依赖、Node.js 和 vim
RUN apt-get update && apt-get install -y --fix-missing \
    curl \
    git \
    gnupg \
    vim \
    && rm -rf /var/lib/apt/lists/*

# 安装 Node.js 18
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# npm 使用国内镜像
RUN npm config set registry https://registry.npmmirror.com

# 安装 Claude Code CLI
RUN npm install -g @anthropic-ai/claude-code

# 创建干净的 Claude Code 配置，只保留必要的模型配置
RUN mkdir -p /root/.claude
RUN echo '{ \
  "env": { \
    "ANTHROPIC_MODEL": "ark-code-latest", \
    "ANTHROPIC_AUTH_TOKEN": "6da7fa7e-de3d-425f-8a68-eafed1221dc4", \
    "ANTHROPIC_BASE_URL": "https://ark.cn-beijing.volces.com/api/coding" \
  }, \
  "model": "ark-code-latest" \
}' > /root/.claude/settings.json

# pip 使用国内镜像，安装 Python 依赖
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple \
    markdown requests beautifulsoup4 html2text

# 设置默认命令
CMD ["bash"]
