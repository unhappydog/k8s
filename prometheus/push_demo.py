# coding=utf-8
import base64
import asyncio
import json,datetime,time
import logging
import prometheus_client
from prometheus_client import Counter,Gauge
from prometheus_client.core import CollectorRegistry
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


class Promethus():
    def __init__(self,promethus_url,job_name = 'response_num'):
        self.loop = asyncio.get_event_loop()  # 获取全局轮训器
        self.job = job_name
        self.promethus_url = promethus_url
        self.registry = CollectorRegistry()   # 存放所有Metrics的容器，以Name-Metric（Key-Value）形式维护其中的Metric对象。
        self.requests_total = Gauge('my_metric_name', 'Total response cout of diff error', ['type','instance'])  # 统计包含一个key（error），使用不同的错误码表示
        self.registry.register(self.requests_total)
        self.push_time=time.time()-5


    # push 数据到prometheus  # 将统计结果push到promethus  不等待结果返回
    def push_prometheus(self):
        logging.info('check push')
        while True:
            try:
                logging.info('begin push to %s' %self.promethus_url)
                self.requests_total.labels('female','pushgateway').inc()
                prometheus_client.push_to_gateway(self.promethus_url, job=self.job, registry=self.registry,timeout=3)  # 设置3秒超时
                # 将所有的error码的统计结果清空
                for label_text in self.requests_total._metrics:
                    self.requests_total._metrics[label_text].set(0)
                logging.info('push success')
                print('push success')

                # 卸载所有搜集器
                # for register in list(self.registry._collector_to_names):
                #     self.registry.unregister(register)


            except Exception as e:
                logging.error('push_to_gateway error %s' %e)

            self.push_time=time.time()
            time.sleep(0.3)    # 每30秒钟push一次



promethus = Promethus(promethus_url='http://192.168.11.127:32225',job_name='my_job_name')

promethus.push_prometheus()


#命令行demo
'''

cat <<EOF | curl --data-binary @- http://192.168.11.127:32225/metrics/job/some_job/instance/some_instance
# TYPE some_metric counter
some_metric{label="val1"} 42
# TYPE another_metric gauge
# HELP another_metric Just an example.
another_metric 2398.283
EOF



cat <<EOF | curl --data-binary @- http://192.168.11.127:32225/metrics/job/111111/instance/22222222
some_metric{label="val1"} 42
another_metric 2398.283
EOF



'''

# 删除数据
# curl -X DELETE http://pushgateway.example.org:9091/metrics/job/some_job/instance/some_instance

# curl -X DELETE http://pushgateway.example.org:9091/metrics/job/some_job