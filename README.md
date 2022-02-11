# aiya-client

## 关于aiya
字母计划系列的首个项目，取哎呀谐音，目标是提供一个C/S结构的本地化工具用于提升办公效率
## 客户端开发语言
Python
## 工具列表
### CutCutCut
大文件通过邮件进行切分发送和收取合并
## python转exe
~~~
pip install pyinstaller
python -m PyInstaller aiya_client.spec
~~~
## 参考文档
* [Python连接RabbitMQ](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)
* [Asynchronous consumer example](https://github.com/pika/pika/blob/master/examples/asynchronous_consumer_example.py)
* [python pika一次消费一条消息](https://blog.csdn.net/lly337/article/details/121925451)
* [pika basic_get](https://pika.readthedocs.io/en/stable/examples/blocking_basic_get.html)