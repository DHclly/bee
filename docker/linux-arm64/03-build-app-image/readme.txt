构建应用镜像，拷贝 python 代码，启动文件到容器

# 构建构建镜像命令，命令在 bee 目录下执行
docker build --platform linux/arm64 --pull=false --tag bee/bee:v1.1.1-arm64 --file docker/linux-arm64/03-build-app-image/Dockerfile .
