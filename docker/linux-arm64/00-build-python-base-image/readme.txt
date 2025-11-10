构建项目基础镜像,提前安装好一些需要的工具，如 curl vim uv

# 拉取 arm64 的镜像
docker pull --platform linux/arm64 python:3.13.3-slim-bookworm

# 重命名标签，带上平台
docker tag  python:3.13.3-slim-bookworm  python:3.13.3-slim-bookworm-arm64

# 构建基础镜像命令，命令在 bee 目录下执行
docker build --platform linux/arm64 --pull=false --tag bee/python-base:3.13.3-slim-bookworm-arm64  --file docker/linux-arm64/00-build-python-base-image/Dockerfile .