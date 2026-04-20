# 公文渲染引擎 V14 - Docker 镜像
# 开源版：包含字体固化 + API服务

FROM python:3.11-slim-bookworm

LABEL maintainer="开源社区"
LABEL version="14.0.0"
LABEL description="公文渲染引擎 - 像素级完美排版"

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    fontconfig \
    libfreetype6 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建字体目录并复制字体
RUN mkdir -p /usr/share/fonts/gongwen
COPY fonts/*.ttf /usr/share/fonts/gongwen/ 2>/dev/null || true
COPY fonts/*.TTF /usr/share/fonts/gongwen/ 2>/dev/null || true

# 刷新字体缓存
RUN fc-cache -fv

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制核心引擎和 API
COPY gongwen_engine.py .
COPY api_server.py .

# 创建输出目录
RUN mkdir -p /app/output

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 启动命令
CMD ["python3", "api_server.py"]
