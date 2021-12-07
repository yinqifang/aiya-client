#!/usr/bin/env phthon
# coding:utf-8

import pika
import yaml


# 获取连接
def get_connection():
    yaml_path = "rabbitmq.yml"

    # 获取mq连接信息
    host = ""
    port = 5672
    username = ""
    password = ""
    with open(yaml_path, 'r', encoding="utf-8") as f:
        config = yaml.safe_load(f)
        mq_config = config["rabbitmq"]
        # print(data)
        host = mq_config["host"]
        port = mq_config["port"]
        username = mq_config["username"]
        password = mq_config["password"]
    # 创建连接
    credentials = pika.PlainCredentials(username=username, password=password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, virtual_host="/",
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

def other():
    print("Other staff....")

if __name__ == '__main__':
    # send()
    receive()
    other()

    # get_connection()
    pass
