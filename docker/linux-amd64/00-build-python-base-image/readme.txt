构建项目基础镜像,提前安装好一些需要的工具，如 curl vim uv

# 拉取 amd64 的镜像
docker pull --platform linux/amd64 python:3.13.3-slim-bookworm

# 重命名标签，带上平台
docker tag  python:3.13.3-slim-bookworm  python:3.13.3-slim-bookworm-amd64

# 构建基础镜像命令，命令在 bee 目录下执行
docker build --platform linux/amd64 --pull=false --tag bee/python-base:3.13.3-slim-bookworm-amd64 --file --file docker/linux-amd64/00-build-python-base-image/Dockerfile .