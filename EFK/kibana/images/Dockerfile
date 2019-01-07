# 下载sentinl-v6.2.4.zip到当前目录
# 在当前文件夹执行 sudo docker build -t luanpeng/lp:kibana-oss-6.2.4 .

FROM registry.cn-beijing.aliyuncs.com/efk-install/kibana-oss:6.2.4

USER root
# 安装插件
RUN yum install vim -y
# RUN /opt/kibana/bin/kibana-plugin install https://github.com/sirensolutions/sentinl/releases/download/tag-6.2.4/sentinl-v6.2.4.zip
COPY ./sentinl-v6.2.4.zip /
RUN /opt/kibana/bin/kibana-plugin install file:///sentinl-v6.2.4.zip
RUN rm /sentinl-v6.2.4.zip

CMD /usr/local/bin/kibana-docker



