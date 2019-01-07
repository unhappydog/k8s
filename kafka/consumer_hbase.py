from kafka import KafkaConsumer
import time
import happybase
import json

hbase_ip = '127.0.0.1'
hbase_port = 9090
ip = hbase_ip
port = hbase_port
pool = happybase.ConnectionPool(size=3, host=ip)


# 往tableName里插数据
def hbase_load(tableName, lists):
    with pool.connection() as connection:
        connection.open()
    if tableName not in str(connection.tables()):
        create_table(connection, tableName)
    # print(tableName,str(connection.tables()))
    table = connection.table(tableName)
    b = table.batch(batch_size=1024)
    for li in lists:
        try:
            rowkey = li['info']
            data_dicts = {}
            for d, x in li.items():
                key = "ss:" + d
                value = str(x)
                data_dicts[key] = value
                b.put(row=rowkey, data=data_dicts)
                b.send()
                print("rowkey:" + rowkey + " data append success")
        except Exception as ex:
            print(str(ex) + " 插入数据失败")

    connection.close()


# 创建HBASE表
def create_table(conn, table):
    try:
        conn.create_table(
            table,
            {
                "ss": dict(max_versions=10)
            }
        )
    except Exception as ex:
        print(str(ex) + " table exists ！！！")


# 打印日志
def log(str):
    t = time.strftime(r"%Y-%m-%d_%H-%M-%S", time.localtime())
    print("[%s]%s" % (t, str))


lst = []
log('start consumer')
# 消费192.168.xxx.xxx:9092上的logfile 这个Topic,指定consumer group是test-consumer-group
consumer = KafkaConsumer('logfile', group_id='test-consumer-group', bootstrap_servers=['192.168.xxx.xxx:9092'])
for msg in consumer:
    recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
    log(recv)
    dict_data = json.loads(msg.value)
    dict_data['info'] = str(dict_data['time']) + '-' + dict_data['pool']
    lst.append(dict_data)
    hbase_load('logfile_zf', lst)
