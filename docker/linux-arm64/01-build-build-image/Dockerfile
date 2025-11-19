# python 底包
FROM bee/python-base:3.13.3-slim-bookworm-arm64 AS build

# 指定工作目录
WORKDIR /app/bee

COPY uv.toml /etc/uv/uv.toml

RUN uv tool install pyclean
