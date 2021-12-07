#!/usr/bin/env phthon
# coding:utf-8

import pika
import yaml
from multiprocessing import Process

# 获取连接
from src.mq.asynchronous_consumer import ReconnectingConsumer


# 获取配置信息
def get_config():
    yaml_path = "rabbitmq.yml"

    rst = {}

    # 获取mq连接信息

    with open(yaml_path, 'r', encoding="utf-8") as f:
        config = yaml.safe_load(f)
        mq_config = config["rabbitmq"]
        # print(data)
        rst["host"] = mq_config["host"]
        rst["port"] = mq_config["port"]
        rst["virtual_host"] = mq_config["virtual_host"]
        rst["username"] = mq_config["username"]
        rst["password"] = mq_config["password"]
    # print(rst)
    return rst


def get_connection():
    yaml_path = "rabbitmq.yml"

    # 获取mq连接信息
    config = get_config()
    # 创建连接
    credentials = pika.PlainCredentials(username=config["username"], password=config["password"])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config["host"], port=config["port"], virtual_host=config["virtual_host"],
                                  credentials=credentials))
    return connection


def send():
    connection = get_connection()
    channel = connection.channel()
    msg = "Hello from python"
    channel.basic_publish(exchange="exchange.aiya", routing_key="routing.aiya", body=msg)
    connection.close()
    print("Sent message to mq")
    pass


def on_message(channel, method_frame, header_frame, body):
    msg = body.decode("utf-8")
    print("Received message: %r" % msg)


def receive():
    connection = get_connection()
    channel = connection.channel()
    channel.basic_consume(queue="queue.aiya", auto_ack=True, on_message_callback=on_message)
    try:
        print("Start consuming...")
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Stopping consuming")
        channel.stop_consuming()
    connection.close()
    print("End receiving")
    pass


def async_receive():
    config = get_config()
    host = config["host"]
    port = config["port"]
    virtual_host = config["virtual_host"]
    username = config["username"]
    password = config["password"]
    queue_name = "queue.aiya"

    consumer = ReconnectingConsumer(host=host, port=port, virtual_host=virtual_host, username=username,
                                    password=password, queue_name=queue_name, on_message=on_message)
    # consumer.run()
    p = Process(target=consumer.run)
    p.start()


def other():
    print("Other staff....")


if __name__ == '__main__':
    # send()
    # receive()
    async_receive()
    other()

    # get_connection()
    pass
