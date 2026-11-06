#!/bin/bash
# 以 docker compose 启动 paddleocr-vl-1.6，若所需网络不存在则先创建
# lf not crlf
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
compose_file="${script_dir}/paddleocr-vl-1.6-compose.yaml"
network=ocr-net

# 网络不存在时创建，已存在则跳过
if ! docker network inspect "$network" >/dev/null 2>&1; then
    echo "[docker-compose] 网络 ${network} 不存在，正在创建"
    docker network create "$network"
fi

echo "[docker-compose] 启动服务 paddleocr-vl-1.6"
docker compose -f "$compose_file" up -d
