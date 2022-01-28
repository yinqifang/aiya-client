import os
import sys

from termcolor import colored

# 添加当前目录到系统路径
cur_file = os.path.abspath(__file__)
cur_path = os.path.sep.join(cur_file.split(os.path.sep)[:-1])
sys.path.append(cur_path)


class ColorPrint:
    @staticmethod
    def print_cyan(prompt):
        ColorPrint.print_color(prompt, 'cyan')

    @staticmethod
    def print_magenta(prompt):
        ColorPrint.print_color(prompt, 'magenta')

    @staticmethod
    def print_green(prompt):
        ColorPrint.print_color(prompt, 'green')

    @staticmethod
    def print_blue(prompt):
        ColorPrint.print_color(prompt, 'blue')

    @staticmethod
    def print_red(prompt):
        ColorPrint.print_color(prompt, 'red')

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


if __name__ == '__main__':
    pass
