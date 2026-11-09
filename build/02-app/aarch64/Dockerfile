FROM dhclly/bee/bee-base:v2.0.0-aarch64

# 指定工作目录
WORKDIR /app

# 暴露端口
EXPOSE 80

COPY app/ .
RUN rm -f .env && chmod +x ./docker-entrypoint.sh ./tini

# 入口点
ENTRYPOINT ["./tini", "--", "./docker-entrypoint.sh"]
