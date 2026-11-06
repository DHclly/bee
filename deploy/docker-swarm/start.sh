#!/bin/bash
# 以 docker swarm 部署 paddleocr-vl-1.6，若所需网络不存在则先创建
# lf not crlf
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
compose_file="${script_dir}/paddleocr-vl-1.6-swarm.yaml"
network=ocr-net
stack=paddleocr-vl-1.6

# overlay 网络不存在时创建，已存在则跳过
if ! docker network inspect "$network" >/dev/null 2>&1; then
    echo "[docker-swarm] 网络 ${network} 不存在，正在创建"
    docker network create --driver overlay "$network"
fi

echo "[docker-swarm] 部署服务栈 ${stack}"
docker stack deploy --detach=true --compose-file "$compose_file" "$stack"
