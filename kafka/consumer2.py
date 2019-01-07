# 使用前要先启动zookeeper和kafka服务
# 启动zookeeper要cd /home/lp/soft/kafka_2.11-1.1.0,然后 bin/zookeeper-server-start.sh config/zookeeper.properties
# 启动kafka要cd /home/lp/soft/kafka_2.11-1.1.0,然后bin/kafka-server-start.sh config/server.properties


from kafka import KafkaConsumer

consumer = KafkaConsumer('test',bootstrap_servers=['127.0.0.1:9092'])  #参数为接收主题和kafka服务器地址

# 这是一个永久堵塞的过程，
for message in consumer:  # consumer是一个消息队列，当后台有消息时，这个消息队列就会自动增加．所以遍历也总是会有数据，当消息队列中没有数据时，就会堵塞等待消息带来
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))





# from kafka import KafkaConsumer
#
# consumer = KafkaConsumer('test',group_id='my-group',bootstrap_servers=['127.0.0.1:9092'])
#
# for message in consumer:
#     print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
#
#

