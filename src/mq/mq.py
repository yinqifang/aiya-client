#!/usr/bin/env phthon
# coding:utf-8
import os
import pika
import yaml
from multiprocessing import Process
# 获取连接
from src.mq.asynchronous_consumer import ReconnectingConsumer
from common.resource_path import Resource

class MQ:
    # 实例
    _instance = None
    # 连接
    _connection = None
    # 队列信息
    _default_exchange = "exchange.aiya"
    _default_routing_key = "routing.aiya"
    _default_queue_name = "queue.aiya"

    # 获取类实例
    @classmethod
    def get_instance(cls):
        if MQ._instance is None:
            MQ._instance = MQ()
        return MQ._instance

    # 获取连接
    def __get_connection(self):
        if MQ._connection is None:
            config = self.__get_config()
            # 创建连接
            credentials = pika.PlainCredentials(username=config["username"], password=config["password"])
            MQ._connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=config["host"], port=config["port"], virtual_host=config["virtual_host"],
                                          credentials=credentials))
        return MQ._connection

    # 获取配置信息
    def __get_config(self):
        # yaml_path = "rabbitmq.yml"
        # yaml_path = os.path.join(os.path.dirname(__file__), "rabbitmq.yml")
        yaml_path = Resource.resource_path("rabbitmq.yml", os.path.dirname(__file__))
        cfg = {}
        # 获取mq连接信息
        with open(yaml_path, 'r', encoding="utf-8") as f:
            config = yaml.safe_load(f)
            mq_config = config["rabbitmq"]
            # print(data)
            cfg["host"] = mq_config["host"]
            cfg["port"] = mq_config["port"]
            cfg["virtual_host"] = mq_config["virtual_host"]
            cfg["username"] = mq_config["username"]
            cfg["password"] = mq_config["password"]
        # print(rst)
        return cfg

    # 发送消息
    def send(self, msg):
        connection = self.__get_connection()
        channel = connection.channel()
        channel.basic_publish(exchange=self._default_exchange, routing_key=self._default_routing_key, body=msg)
        # connection.close()
        # print("Sent message to mq")

    # 拉取一条消息
    def get(self):
        connection = self.__get_connection()
        channel = connection.channel()
        method_frame, header_frame, body = channel.basic_get(queue=self._default_queue_name, auto_ack=False)
        if method_frame:
            # print(method_frame, header_frame, body)
            channel.basic_ack(method_frame.delivery_tag)
            return str(body, 'utf-8')
        else:
            # print('No message returned')
            return None

    def on_message(channel, method_frame, header_frame, body):
        msg = body.decode("utf-8")
        print("Received message: %r" % msg)

    def receive(self):
        connection = self.__get_connection()
        channel = connection.channel()
        channel.basic_consume(queue=self._default_queue_name, auto_ack=True, on_message_callback=self.on_message)
        try:
            print("Start consuming...")
            channel.start_consuming()
        except KeyboardInterrupt:
            print("Stopping consuming")
            channel.stop_consuming()
        # connection.close()
        print("End receiving")
        pass

    def async_receive(self):
        config = self.get_config()
        host = config["host"]
        port = config["port"]
        virtual_host = config["virtual_host"]
        username = config["username"]
        password = config["password"]
        queue_name = self._default_queue_name

        consumer = ReconnectingConsumer(host=host, port=port, virtual_host=virtual_host, username=username,
                                        password=password, queue_name=queue_name, on_message=self.on_message)
        # consumer.run()
        p = Process(target=consumer.run)
        p.start()

    # 关闭连接
    def close(self):
        if MQ._connection is not None:
            MQ._connection.close()


if __name__ == '__main__':
    # send()
    # receive()
    # async_receive()

    # get_connection()
    pass
