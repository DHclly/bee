#!/bin/bash
# 把 paddleocr-vl-1.6 的副本数各减少 1，每次执行只减一个。
#
# 用法: ./scale-down.sh [server|api|all]
# lf not crlf
set -euo pipefail

stack=paddleocr-vl-1.6
target_scope="${1:-all}"

# 完整服务名由栈名加 yaml 中的服务名组成；缩容先缩 api 再缩 server
services=()
case "$target_scope" in
    server) services=("${stack}_paddleocr-vl-server-runner") ;;
    api) services=("${stack}_paddleocr-vl-api-runner") ;;
    all)
        services=(
            "${stack}_paddleocr-vl-api-runner"
            "${stack}_paddleocr-vl-server-runner"
        )
        ;;
    *) echo "错误: 参数只能是 server、api 或 all (got: '$target_scope')" >&2; exit 1 ;;
esac

for service in "${services[@]}"; do
    current=$(docker service inspect "$service" --format '{{.Spec.Mode.Replicated.Replicas}}')
    if [ "$current" -le 0 ]; then
        echo "[scale-down] ${service} 副本数已为 0，跳过"
        continue
    fi
    next=$((current - 1))
    echo "[scale-down] ${service} 副本数 ${current} -> ${next}"
    docker service scale "${service}=${next}"
done
