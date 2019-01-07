

import prometheus_client
from prometheus_client import Counter,Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
import random

app = Flask(__name__)

# metrics包含
requests_total = Counter("request_count", "Total request cout of the host")  # 数值只增
random_value = Gauge("random_value", "Random value of the request")  # 数值可大可小



@app.route("/metrics")
def requests_count():

    requests_total.inc()     # 计数器自增
    # requests_total.inc(2)
    return Response(prometheus_client.generate_latest(requests_total),mimetype="text/plain")   # 将计数器的值返回

@app.route("/metrics2")
def r_value():
    random_value.set(random.randint(0, 10))   # 设置值任意值，但是一定要为 整数或者浮点数
    return Response(prometheus_client.generate_latest(random_value),mimetype="text/plain")    # 将值返回

@app.route('/')
def index():
    requests_total.inc()
    return "Hello World"






# 使用labels来区分metric的特征

c = Counter('requests_total', 'HTTP requests total', ['method', 'clientip'])  # 添加lable的key，

c.labels('get', '127.0.0.1').inc()       #为不同的label进行统计
c.labels('post', '192.168.0.1').inc(3)     #为不同的label进行统计
c.labels(method="get", clientip="192.168.0.1").inc()   #为不同的label进行统计

g = Gauge('my_inprogress_requests', 'Description of gauge',['mylabelname'])
g.labels(mylabelname='str').set(3.6)    #value自己定义,但是一定要为 整数或者浮点数





if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8888)