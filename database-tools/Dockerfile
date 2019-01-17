FROM registry.cn-hangzhou.aliyuncs.com/boldseas/alpine-oraclejdk8:0.2
RUN mkdir -p /root/db_tools
WORKDIR /root/db_tools
COPY build/install .
RUN chmod +x ./database-tools/bin/database-tools
CMD ["./database-tools/bin/database-tools"]
