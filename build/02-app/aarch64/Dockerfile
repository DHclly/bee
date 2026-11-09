ARG BASE_IMAGE=dhclly/bee/bee-base:v2.0.0-aarch64
FROM ${BASE_IMAGE}

# 指定工作目录
WORKDIR /app

# 暴露端口
EXPOSE 80

COPY app/ .
RUN rm -f .env /app/tini /app/docker-entrypoint.sh

COPY app/tini /tini
COPY app/docker-entrypoint.sh /docker-entrypoint.sh

# 设置权限
RUN chmod +x /docker-entrypoint.sh /tini

# 入口点
ENTRYPOINT ["/tini", "--", "/docker-entrypoint.sh"]
