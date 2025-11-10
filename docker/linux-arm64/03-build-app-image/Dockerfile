FROM bee/bee-build:v1.0.1-arm64 AS build

# 指定工作目录
WORKDIR /app/bee

COPY src .
COPY README.md ./README.md

RUN uv tool run pyclean .

FROM bee/bee-publish:v1.0.1-arm64 AS publish

# 指定工作目录
WORKDIR /app/bee

# 暴露端口
EXPOSE 80

COPY docker/linux-arm64/app-context/tini /tini
COPY docker/linux-arm64/app-context/docker-entrypoint.sh /docker-entrypoint.sh

# 设置权限
RUN chmod +x /docker-entrypoint.sh /tini

COPY --from=build /app/bee .

# 入口点
ENTRYPOINT ["/tini", "--", "/docker-entrypoint.sh"]