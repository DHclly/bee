
## 构建命令

```
./build.sh manual 2.0.0 x86_64

./build.sh manual 2.0.0 aarch64
```

## 基础底包 python:3.13.3 镜像地址

### amd64

docker pull --platform linux/amd64 python:3.13.3-slim-bookworm

docker pull --platform=linux/amd64 docker.1ms.run/python:3.13.3-slim-bookworm

docker tag docker.1ms.run/python:3.13.3-slim-bookworm python:3.13.3-slim-bookworm-amd64

### arm64

docker pull --platform linux/arm64 python:3.13.3-slim-bookworm

docker pull --platform=linux/arm64 docker.1ms.run/python:3.13.3-slim-bookworm

docker tag docker.1ms.run/python:3.13.3-slim-bookworm python:3.13.3-slim-bookworm-arm64