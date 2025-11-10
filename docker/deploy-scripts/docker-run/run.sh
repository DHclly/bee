docker run -d --name=bee \
-e bee_embeddings_url= \
-e bee_rerank_url= \
-e bee_chat_url= \
-e bee_provider_type=gpustack \
-p 8090:80 \
bee/bee:v1.1.0-arm64
