# 正常启动命令
docker run -d --name=bee \
-e bee_embeddings_url=http://localhost/v1/embeddings \
-e bee_rerank_url=http://localhost/v1/rerank \
-e bee_chat_url=http://localhost/v1/chat/completions \
-e bee_provider_type=gpustack \
-p 8090:80 \
bee/bee:v1.1.2-amd64

# 在低版本docker（docker version <=20.x）下可能起不来,尝试着命令
docker run -d --name=bee \
  --security-opt seccomp=unconfined \
  --cap-add=SYS_PTRACE \
  -e bee_embeddings_url=http://localhost/v1/embeddings \
  -e bee_rerank_url=http://localhost/v1/rerank \
  -e bee_chat_url=http://localhost/v1/chat/completions \
  -e bee_provider_type=gpustack \
  -p 8090:80 \
  bee/bee:v1.1.2-amd64

# 还不行就尝试着
docker run -d --name=bee \
--privileged \
-e bee_embeddings_url=http://localhost/v1/embeddings \
-e bee_rerank_url=http://localhost/v1/rerank \
-e bee_chat_url=http://localhost/v1/chat/completions \
-e bee_provider_type=gpustack \
-p 8090:80 \
bee/bee:v1.1.2-amd64


