#!/usr/bin/env phthon
# coding:utf-8
import json
import os
import yaml
import requests
from multiprocessing import Process
# 获取连接
from common.resource_path import Resource
from common.config_reader import ConfigReader
from common.color_print import ColorPrint

# Http方式的mq消息处理，用于处理无法直接连接MQ的情形
class MQHttp:
    # 实例
    _instance = None
    # 队列信息
    _default_exchange = "exchange.aiya"
    _default_routing_key = "routing.aiya"
    _default_queue_name = "queue.aiya"

    # 获取类实例
    @classmethod
    def get_instance(cls):
        if MQHttp._instance is None:
            MQHttp._instance = MQHttp()
        return MQHttp._instance

    # 获取配置信息
    def __get_config(self):
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

    # 获取代理信息
    def __get_proxy(self):
        proxies = {}
        config_reader = ConfigReader.get_instance()
        section = 'proxy'
        config_key = 'proxy.http'
        http_proxy = config_reader.read_config(config_reader.get_config_file(), section, config_key)
        if http_proxy is not None and len(http_proxy) > 0:
            proxies['http'] = http_proxy
        if ConfigReader.get_instance().is_debug_on():
            print("Proxies : " + str(proxies))
        return proxies

    # 发送消息
    def send(self, msg):
        config_reader = ConfigReader.get_instance()
        section = 'mq.http'
        config_key = 'mq.url.send'
        url = config_reader.read_config(config_reader.get_config_file(), section, config_key)
        if url is None:
            ColorPrint.get_instance().print_red("配置文件缺少" + config_key + "配置！")
            return
        payload = {'exchangeName': self._default_exchange, 'routingKey': self._default_routing_key, 'msg': msg}

        resp = requests.post(url=url, json=payload, proxies=self.__get_proxy())
        if resp.status_code == 200:
            ColorPrint.get_instance().print_green("发送成功: " + str(resp.text)[0:20] + "...")
        else:
            ColorPrint.get_instance().print_red("发送失败：" + str(resp.text))

    # 拉取一条消息
    def get(self):
        config_reader = ConfigReader.get_instance()
        section = 'mq.http'
        config_key = 'mq.url.get'
        url = config_reader.read_config(config_reader.get_config_file(), section, config_key)
        if url is None:
            ColorPrint.get_instance().print_red("配置文件缺少" + config_key + "配置！")
            return
        payload = {'queueName': self._default_queue_name}

        resp = requests.post(url=url, json=payload, proxies=self.__get_proxy())
        if resp.status_code == 200:
            if len(resp.text) == 0:
                if ConfigReader.get_instance().is_debug_on():
                    ColorPrint.get_instance().print_magenta("没有发现新消息")
            else:
                ColorPrint.get_instance().print_green("接收成功: " + str(resp.text)[0:20] + "...")
            return resp.text
        else:
            ColorPrint.get_instance().print_red("接收失败：" + str(resp.text))
            return None


if __name__ == '__main__':
    # MQHttp.get_instance().send("Hello mq!")
    # MQHttp.get_instance().get()
    pass
