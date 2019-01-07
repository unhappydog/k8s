# sudo docker build -t cloud-prometheus:1.0.0 .

FROM prom/prometheus

# 复制所需要文件夹进入
COPY ./alert.rules /etc/prometheus/
COPY ./prometheus.yml /etc/prometheus/

# 清理工作
CMD sleep 3000
