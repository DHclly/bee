#!/bin/bash
# 停止 paddleocr-vl-1.6 的 k8s 资源，先停 api 再停 server
# lf not crlf
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[k8s] 停止 api"
kubectl delete -f "${script_dir}/paddleocr-vl-1.6-api-k8s.yaml"

echo "[k8s] 停止 server"
kubectl delete -f "${script_dir}/paddleocr-vl-1.6-server-k8s.yaml"
