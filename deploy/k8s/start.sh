#!/bin/bash
# 以 k8s 启动 paddleocr-vl-1.6，先起 server 再起 api
# lf not crlf
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[k8s] 启动 server"
kubectl apply -f "${script_dir}/paddleocr-vl-1.6-server-k8s.yaml"

echo "[k8s] 启动 api"
kubectl apply -f "${script_dir}/paddleocr-vl-1.6-api-k8s.yaml"
