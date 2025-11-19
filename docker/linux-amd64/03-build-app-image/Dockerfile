FROM bee/bee-build:v1.0.1-amd64 AS build

# 指定工作目录
WORKDIR /app/bee

COPY src .
RUN rm -f .env
COPY README.md ./README.md
COPY change_log.txt ./change_log.txt
COPY .python-version ./.python-version

RUN uv tool run pyclean .

FROM bee/bee-publish:v1.0.1-amd64 AS publish

# 指定工作目录
WORKDIR /app/bee

# 暴露端口
EXPOSE 80

COPY docker/linux-amd64/app-context/tini /tini
COPY docker/linux-amd64/app-context/docker-entrypoint.sh /docker-entrypoint.sh

# 设置权限
RUN chmod +x /docker-entrypoint.sh /tini

COPY --from=build /app/bee .

# 入口点
ENTRYPOINT ["/tini", "--", "/docker-entrypoint.sh"]