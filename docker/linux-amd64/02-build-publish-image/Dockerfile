# python 底包
FROM bee/python-base:3.13.3-slim-bookworm-amd64 AS publish

# 指定工作目录
WORKDIR /app/bee

COPY src/uv.toml /etc/uv/uv.toml
COPY src/pyproject.toml src/uv.toml ./

RUN uv lock && uv sync --frozen --no-dev