#!/bin/bash
# 启动 paddleocr-vl-1.6 的 server 与 api 容器，若所需网络不存在则先创建
# lf not crlf
set -euo pipefail

network=ocr-net
server_container=paddleocr-vl-server-runner
api_container=paddleocr-vl-api-runner

# server 镜像与端口
server_image=dev.registry.edoc2.com/edoc2v5/paddleocr-vl-1.6-server:v1.0.0-x86_64
server_port=8219

# api 镜像与端口
api_image=dev.registry.edoc2.com/edoc2v5/paddleocr-vl-1.6-api:v1.0.0-x86_64
api_port=8220

# 网络不存在时创建，已存在则跳过
if ! docker network inspect "$network" >/dev/null 2>&1; then
    echo "[docker-start] 网络 ${network} 不存在，正在创建"
    docker network create "$network"
fi

# 旧容器存在时先移除，避免容器名冲突
for container in "$server_container" "$api_container"; do
    if docker container inspect "$container" >/dev/null 2>&1; then
        echo "[docker-start] 移除已有容器 ${container}"
        docker rm -f "$container"
    fi
done

echo "[docker-start] 启动容器 ${server_container}"

docker run -itd --name="$server_container" \
  --security-opt seccomp=unconfined \
  --restart=unless-stopped \
  --cap-add=SYS_PTRACE \
  --network "$network" \
  -e CUDA_DEVICE_ORDER=PCI_BUS_ID \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e CUDA_VISIBLE_DEVICES=0 \
  -e INWISEAI_PROCESS_VRAM=8 \
  -p "${server_port}:8000" \
  "$server_image"

echo "[docker-start] 启动容器 ${api_container}"

# api 内的 paddlex 通过容器名 paddleocr-vl-server-runner 访问 server，
# 需先等 server 就绪；api 侧的 vllm 探活失败不影响识别，可先启动
docker run -itd --name="$api_container" \
  --security-opt seccomp=unconfined \
  --restart=unless-stopped \
  --cap-add=SYS_PTRACE \
  --network "$network" \
  -e CUDA_DEVICE_ORDER=PCI_BUS_ID \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e CUDA_VISIBLE_DEVICES=0 \
  -e INWISEAI_PROCESS_VRAM=1 \
  -p "${api_port}:8000" \
  "$api_image"

echo "[docker-start] 已启动"
echo "  server: http://localhost:${server_port}"
echo "  api   : http://localhost:${api_port}"
