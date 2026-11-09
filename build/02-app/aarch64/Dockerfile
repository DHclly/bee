FROM dhclly/bee/bee-base:v2.0.0-aarch64 AS build

# 指定工作目录
WORKDIR /app/bee

COPY app/ .
RUN rm -f .env /app/bee/tini /app/bee/docker-entrypoint.sh

RUN uv tool run pyclean .

FROM bee/bee-publish:v1.0.1-arm64 AS publish

# 指定工作目录
WORKDIR /app/bee

# 暴露端口
EXPOSE 80

COPY app/tini /tini
COPY app/docker-entrypoint.sh /docker-entrypoint.sh

# 设置权限
RUN chmod +x /docker-entrypoint.sh /tini

COPY --from=build /app/bee .

# 入口点
ENTRYPOINT ["/tini", "--", "/docker-entrypoint.sh"]