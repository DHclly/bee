#!/bin/bash

# 提高脚本健壮性：出错停止、未定义变量报错、管道错误传播
set -euo pipefail  

cd /app/bee
source .venv/bin/activate

echo "Starting Bee..."
echo "Welcome to Bee, a lightweight LLM API proxy."

# 从环境变量 bee_workers 读取 worker 数量，默认为 1
bee_workers="${bee_workers:-1}"

# 可选：验证 bee_workers 是正整数（增强健壮性）
if ! [[ "$bee_workers" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: bee_workers must be a positive integer (got: '$bee_workers')" >&2
    exit 1
fi

echo "Using ${bee_workers} worker(s)..."

# 执行主服务，替换当前进程
exec uvicorn main:app --host 0.0.0.0 --port 80 --bee_workers "$bee_workers"