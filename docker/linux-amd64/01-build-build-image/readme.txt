构建构建镜像，安装一些构建工具，目前装了 pyclean

- pyclean: 清理 __pycache__ *.pyc 文件


# 构建构建镜像命令，命令在 bee 目录下执行
docker build --platform linux/amd64 --pull=false --tag bee/bee-build:v1.0.1-amd64 --file docker/linux-amd64/01-build-build-image/Dockerfile .

