FROM dhclly/bee/bee-base:v2.0.0-x86_64

# 指定工作目录
WORKDIR /app

# 暴露端口
EXPOSE 80

COPY app/ .
RUN chmod +x /app/docker-entrypoint.sh /app/tini

# 入口点
ENTRYPOINT ["/app/tini", "--", "/app/docker-entrypoint.sh"]
