#!/bin/bash
# 把 paddleocr-vl-1.6 的副本数各减少 1，每次执行只减一个。
#
# 用法: ./scale-down.sh [server|api|all]
# lf not crlf
set -euo pipefail

namespace=edoc2
target_scope="${1:-all}"

# 缩容时先缩 api 再缩 server，避免 api 先失去推理能力
case "$target_scope" in
    server) deployments=(paddleocr-vl-server-runner) ;;
    api) deployments=(paddleocr-vl-api-runner) ;;
    all) deployments=(paddleocr-vl-api-runner paddleocr-vl-server-runner) ;;
    *) echo "错误: 参数只能是 server、api 或 all (got: '$target_scope')" >&2; exit 1 ;;
esac

for deployment in "${deployments[@]}"; do
    current=$(kubectl -n "$namespace" get deployment "$deployment" -o jsonpath='{.spec.replicas}')
    if [ "$current" -le 0 ]; then
        echo "[scale-down] ${deployment} 副本数已为 0，跳过"
        continue
    fi
    next=$((current - 1))
    echo "[scale-down] ${deployment} 副本数 ${current} -> ${next}"
    kubectl -n "$namespace" scale deployment "$deployment" --replicas="$next"
done
