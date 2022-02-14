import time
import os
import traceback
from common.color_print import ColorPrint
from common.clipboard import Clipboard
from cut_cut_cut.cut_cut_cut import CutCutCut
from mq.mq import MQ
from common.resource_path import Resource

class AiyaClient:
    # 定义参数
    _version_ = '1.1'

    # 主流程
    def main(self):
        print("欢迎使用哎呀(V" + self._version_ + ")")
        ColorPrint.get_instance().print_red("本工具仅供内部研究使用，请注意信息安全，由此带来的一切后果与作者无关（手动狗头）")

        # 菜单选择
        self.print_menu()
        selected = self.select_menu()
        while selected != "quit":
            try:
                if selected == "cut":
                    # 切切切
                    CutCutCut().main()
                elif selected == "cc":
                    # 发送粘贴板
                    # print("发送粘贴板")
                    data = Clipboard.get_data_from_clipboard()
                    print("粘贴板数据：" + data[0:20] + "...")
                    MQ.get_instance().send(data)
                    ColorPrint.get_instance().print_blue("已发送到MQ!")
                elif selected == "cv":
                    # 接收到粘贴板
                    data = MQ.get_instance().get()
                    if data is None:
                        ColorPrint.get_instance().print_red("没有找到数据")
                    else:
                        Clipboard.write_data_to_clipboard(data)
                        print("收到数据：" + data[0:20] + "...")
                        ColorPrint.get_instance().print_green("数据已成功复制到粘贴板！")
                elif selected == "8":
                    # 更新日志
                    self.print_release_notes()
                elif selected == "9":
                    # 查看菜单
                    self.print_menu()
                else:
                    # 错误输入
                    print("输入错误，请重新输入！")
            except Exception as e:
                print(traceback.format_exc())
                # print(e)
            selected = self.select_menu()
        print("谢谢使用，再见！")

    # 显示菜单
    def print_menu(self):
        ColorPrint.get_instance().print_green("cut： 切切切")
        ColorPrint.get_instance().print_green("cc： 发送粘贴板")
        ColorPrint.get_instance().print_green("cv： 接收到粘贴板")
        ColorPrint.get_instance().print_green("8： 更新日志")
        ColorPrint.get_instance().print_magenta("quit： 退出")

    # 菜单选择
    def select_menu(self):
        return input("请输入要使用的功能（9菜单，quit退出）：")

    # 显示更新日志
    def print_release_notes(self):
        # 获取当前目录
        # f = open(self.resource_path("cut_cut_cut_release_notes.txt"), "r", encoding='utf-8')
        f = open(Resource.resource_path("release_notes.txt", os.path.dirname(__file__)), "r", encoding='utf-8')
        print(f.read())

if __name__ == '__main__':
    AiyaClient().main()
    pass
