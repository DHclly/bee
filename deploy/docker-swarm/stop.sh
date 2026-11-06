#!/bin/bash
# 移除 paddleocr-vl-1.6 的 swarm 服务栈
# lf not crlf
set -euo pipefail

stack=paddleocr-vl-1.6

echo "[docker-swarm] 移除服务栈 ${stack}"
docker stack rm "$stack"
