#!/bin/bash
# 停止并移除 paddleocr-vl-1.6 的 compose 服务
# lf not crlf
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
compose_file="${script_dir}/paddleocr-vl-1.6-compose.yaml"

echo "[docker-compose] 停止服务 paddleocr-vl-1.6"
docker compose -f "$compose_file" down
