构建应用镜像，拷贝 python 代码，启动文件到容器

# 构建构建镜像命令，命令在 bee 目录下执行

# 2025.11.20

docker build --platform linux/amd64 --pull=false --tag bee/bee:v1.3.6-amd64 --file docker/linux-amd64/03-build-app-image/Dockerfile .
docker build --platform linux/amd64 --pull=false --tag bee/bee:v1.3.5-amd64 --file docker/linux-amd64/03-build-app-image/Dockerfile .
docker build --platform linux/amd64 --pull=false --tag bee/bee:v1.3.3-amd64 --file docker/linux-amd64/03-build-app-image/Dockerfile .
docker build --platform linux/amd64 --pull=false --tag bee/bee:v1.3.0-amd64 --file docker/linux-amd64/03-build-app-image/Dockerfile .


# 2025.11.13

docker build --platform linux/amd64 --pull=false --tag bee/bee:v1.2.1-amd64 --file docker/linux-amd64/03-build-app-image/Dockerfile .


# 2025.11.11

docker build --platform linux/amd64 --pull=false --tag bee/bee:v1.1.2-amd64 --file docker/linux-amd64/03-build-app-image/Dockerfile .

# 2025.11.10

docker build --platform linux/amd64 --pull=false --tag bee/bee:v1.1.0-amd64 --file docker/linux-amd64/03-build-app-image/Dockerfile .

