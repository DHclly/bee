构建应用镜像，拷贝 python 代码，启动文件到容器

# 构建构建镜像命令，命令在 bee 目录下执行

# 2025.11.13

docker build --platform linux/arm64 --pull=false --tag bee/bee:v1.2.1-arm64 --file docker/linux-arm64/03-build-app-image/Dockerfile .

# 2025.11.12

docker build --platform linux/arm64 --pull=false --tag bee/bee:v1.2.0-arm64 --file docker/linux-arm64/03-build-app-image/Dockerfile .
docker build --platform linux/arm64 --pull=false --tag bee/bee:v1.1.7-arm64 --file docker/linux-arm64/03-build-app-image/Dockerfile .
docker build --platform linux/arm64 --pull=false --tag bee/bee:v1.1.6-arm64 --file docker/linux-arm64/03-build-app-image/Dockerfile .
docker build --platform linux/arm64 --pull=false --tag bee/bee:v1.1.5-arm64 --file docker/linux-arm64/03-build-app-image/Dockerfile .
docker build --platform linux/arm64 --pull=false --tag bee/bee:v1.1.4-arm64 --file docker/linux-arm64/03-build-app-image/Dockerfile .
docker build --platform linux/arm64 --pull=false --tag bee/bee:v1.1.3-arm64 --file docker/linux-arm64/03-build-app-image/Dockerfile .

# 2025.11.11

docker build --platform linux/arm64 --pull=false --tag bee/bee:v1.1.2-arm64 --file docker/linux-arm64/03-build-app-image/Dockerfile .

# 2025.11.10

docker build --platform linux/arm64 --pull=false --tag bee/bee:v1.1.1-arm64 --file docker/linux-arm64/03-build-app-image/Dockerfile .
