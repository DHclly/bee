#!/bin/bash
# 把 paddleocr-vl-1.6 的副本数各增加 1，每次执行只加一个。
#
# 用法: ./scale-up.sh [server|api|all]
# lf not crlf
set -euo pipefail

namespace=edoc2
target_scope="${1:-all}"

case "$target_scope" in
    server) deployments=(paddleocr-vl-server-runner) ;;
    api) deployments=(paddleocr-vl-api-runner) ;;
    all) deployments=(paddleocr-vl-server-runner paddleocr-vl-api-runner) ;;
    *) echo "错误: 参数只能是 server、api 或 all (got: '$target_scope')" >&2; exit 1 ;;
esac

for deployment in "${deployments[@]}"; do
    current=$(kubectl -n "$namespace" get deployment "$deployment" -o jsonpath='{.spec.replicas}')
    next=$((current + 1))
    echo "[scale-up] ${deployment} 副本数 ${current} -> ${next}"
    kubectl -n "$namespace" scale deployment "$deployment" --replicas="$next"
done
