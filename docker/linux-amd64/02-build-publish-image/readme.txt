构建发布镜像，安装项目依赖的 python 包

# 构建构建镜像命令，命令在 bee 目录下执行
docker build --platform linux/amd64 --pull=false --tag bee/bee-publish:v1.0.1-amd64 --file docker/linux-amd64/02-build-publish-image/Dockerfile .

