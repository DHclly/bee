#!/bin/bash

# 提高脚本健壮性：出错停止、未定义变量报错、管道错误传播
set -euo pipefail  

cd /app/bee
source .venv/bin/activate

echo "Starting Bee..."
echo "Welcome to Bee, a lightweight LLM API proxy."

# 执行主服务，替换当前进程
exec uvicorn main:app --host 0.0.0.0 --port 80 --workers 1