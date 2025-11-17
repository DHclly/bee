import httpx


class HttpClientManager:
    def __init__(self):
        self.embeddings_client:httpx.AsyncClient
        self.rerank_client:httpx.AsyncClient
        self.chat_client:httpx.AsyncClient

    async def startup(self):
        self.embeddings_client = httpx.AsyncClient(timeout=httpx.Timeout(
            connect=3.0,
            read=60.0,
            write=30.0,
            pool=5.0
        ))
        
        self.rerank_client = httpx.AsyncClient(timeout=httpx.Timeout(
            connect=3.0,
            read=60.0,
            write=310.0,
            pool=5.0
        ))
        
        self.chat_client = httpx.AsyncClient(timeout=httpx.Timeout(
            connect=3.0,   # 连接服务器最多 3 秒
            read=300.0,     # 读取响应最多 30 秒（适合大响应或慢模型）
            write=30.0,    # 发送请求最多 10 秒
            pool=5.0       # 等待连接池最多 5 秒
        ))

    async def shutdown(self):
        if self.embeddings_client:
            await self.embeddings_client.aclose()
        if self.rerank_client:
            await self.rerank_client.aclose()
        if self.chat_client:
            await self.chat_client.aclose()

http_clients = HttpClientManager()
