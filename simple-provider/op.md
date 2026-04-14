记录快速适配记录

## 构建历史记录

### 2026.04.14

docker build --platform linux/amd64 --pull=false --tag bee/bee:v1.3.9-amd64-p1 --file Dockerfile .

docker run -d --name=bee-p1 bee/bee:v1.3.9-amd64-p1