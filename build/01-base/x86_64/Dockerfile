FROM python:3.13.3-slim-bookworm-amd64 AS base
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo 'Asia/Shanghai' >/etc/timezone && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        ssh \
        curl \
        vim \
        lsb-release &&\
        apt-get clean && \
        rm -rf /var/lib/apt/lists/* && \
        pip install --no-cache-dir \
        uv

# 指定工作目录
WORKDIR /app

COPY app/uv.toml /etc/uv/uv.toml
COPY app/pyproject.toml app/uv.toml ./

RUN uv lock && uv sync --frozen --no-dev