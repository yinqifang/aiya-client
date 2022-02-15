import os
import configparser


# ----- 从文件中读写配置 ----
import sys


class ConfigReader:
    root_path = None

    # 读取配置，使用指定配置文件
    def read_config(self, config_file, section, config_key):
        try:
            if not os.path.exists(config_file):
                # print("config file not exist!: " + config_file)
                return None
            conf = configparser.ConfigParser()
            conf.read(config_file)
            return conf.get(section, config_key)
        except Exception as e:
            # print(traceback.format_exc())
            return None

    # 写入配置，使用指定配置文件
    def write_config(self, config_file, section, config_key, config_val):
        try:
            conf = configparser.ConfigParser()
            conf.read(config_file)
            # 添加section
            if not conf.has_section(section):
                conf.add_section(section)
            # 预备要写入配置文件的字段
            conf.set(section, config_key, str(config_val))
            # 开始写入配置文件,如果文件不存在则创建一个文件
            with open(config_file, 'w') as fw:
                conf.write(fw)
        except Exception as e:
            # print(traceback.format_exc())
            pass

    # 获取配置文件
    def get_config_file(self):
        return os.path.join(ConfigReader.root_path, "AiyaClient.conf")

    def __init__(self):
        # ConfigReader.root_path = os.path.dirname(__file__)    // src可行，exe不行
        # ConfigReader.root_path = os.path.dirname(sys.executable)  // src下不行，exe可行
        # ConfigReader.root_path = sys.path[0]  // src可行，exe不行
        # ConfigReader.root_path = os.getcwd() // src可行，exe不行

        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            sys._MEIPASS    # 用于环境监测
            # 当前是exe环境
            ConfigReader.root_path = os.path.dirname(sys.executable)
        except Exception:
            # 当前是非exe环境
            ConfigReader.root_path = os.getcwd()

        print("Config file root path: " + ConfigReader.root_path)
