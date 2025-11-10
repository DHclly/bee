FROM python:3.13.3-slim-bookworm-arm64 AS base
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