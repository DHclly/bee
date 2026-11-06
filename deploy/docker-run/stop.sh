#!/bin/bash
# 停止并删除 paddleocr-vl-1.6 的 api 与 server 容器，容器不存在时直接跳过
# lf not crlf
set -euo pipefail

# api 依赖 server，先停 api
containers=(paddleocr-vl-api-runner paddleocr-vl-server-runner)

for container in "${containers[@]}"; do
    # 容器不存在时无需处理，避免报错
    if ! docker container inspect "$container" >/dev/null 2>&1; then
        echo "[docker-stop] 容器 ${container} 不存在，无需处理"
        continue
    fi

    echo "[docker-stop] 停止容器 ${container}"
    docker stop "$container"

    echo "[docker-stop] 删除容器 ${container}"
    docker rm -f "$container"
done

echo "[docker-stop] 已清理完成"
