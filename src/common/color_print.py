import os
import sys

import colorama
from termcolor import colored

# 添加当前目录到系统路径
cur_file = os.path.abspath(__file__)
cur_path = os.path.sep.join(cur_file.split(os.path.sep)[:-1])
sys.path.append(cur_path)


class ColorPrint:
    _instance = None

    @classmethod
    def get_instance(cls):
        if ColorPrint._instance is None:
            ColorPrint._instance = ColorPrint()
        return ColorPrint._instance

    # @staticmethod
    def print_cyan(self, prompt):
        self.print_color(prompt, 'cyan')

    # @staticmethod
    def print_magenta(self, prompt):
        self.print_color(prompt, 'magenta')

    # @staticmethod
    def print_green(self, prompt):
        self.print_color(prompt, 'green')

    # @staticmethod
    def print_blue(self, prompt):
        self.print_color(prompt, 'blue')

    # @staticmethod
    def print_red(self, prompt):
        self.print_color(prompt, 'red')

    @staticmethod
    def print_color(prompt, color):
        print(colored(prompt, color))

    @staticmethod
    def blue(prompt):
        return colored(prompt, "blue")

    @staticmethod
    def cyan(prompt):
        return colored(prompt, "cyan")

    @staticmethod
    def green(prompt):
        return colored(prompt, "green")

    @staticmethod
    def magenta(prompt):
        return colored(prompt, "magenta")

    @staticmethod
    def red(prompt):
        return colored(prompt, "red")

    @staticmethod
    def yellow(prompt):
        return colored(prompt, "yellow")

    def __init__(self):
        # 初始化，否则打成exe包后会显示乱码
        colorama.init()


if __name__ == '__main__':
    pass
