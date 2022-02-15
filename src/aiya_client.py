import time
import os
import traceback
from common.color_print import ColorPrint
from common.clipboard import Clipboard
from cut_cut_cut.cut_cut_cut import CutCutCut
from mq.mq_http import MQHttp
from common.resource_path import Resource

class AiyaClient:
    # 定义参数
    _version_ = '1.2'

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
                elif selected == "send":
                    # 发送粘贴板数据
                    data = Clipboard.get_data_from_clipboard()
                    if data is None or len(data) == 0:
                        ColorPrint.get_instance().print_red("粘贴板数据为空！")
                    else:
                        # print("粘贴板数据：" + data[0:20] + "...")
                        MQHttp.get_instance().send(data)
                        # ColorPrint.get_instance().print_blue("已发送到MQ!")
                elif selected == "get":
                    # 接收数据到粘贴板
                    data = MQHttp.get_instance().get()
                    if data is None or len(data) == 0:
                        ColorPrint.get_instance().print_red("没有找到数据")
                    else:
                        Clipboard.write_data_to_clipboard(data)
                        # print("收到数据：" + data[0:20] + "...")
                        ColorPrint.get_instance().print_green("数据已成功复制到粘贴板！")
                elif selected == "log":
                    # 更新日志
                    self.print_release_notes()
                elif selected == "help" or selected == "h" or selected == "?":
                    # 查看帮助
                    self.print_help()
                elif selected == "menu" or selected == "m" or selected == "9":
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
        ColorPrint.get_instance().print_green("send： 发送粘贴板数据")
        ColorPrint.get_instance().print_green("get： 接收数据到粘贴板")
        ColorPrint.get_instance().print_green("log： 更新日志")
        ColorPrint.get_instance().print_magenta("quit： 退出")

    # 菜单选择
    def select_menu(self):
        return input("请输入要使用的功能（menu/m/9菜单，help/h/?帮助，quit退出）：")

    # 显示更新日志
    def print_release_notes(self):
        # 获取当前目录
        # f = open(self.resource_path("cut_cut_cut_release_notes.txt"), "r", encoding='utf-8')
        f = open(Resource.resource_path("release_notes.txt", os.path.dirname(__file__)), "r", encoding='utf-8')
        print(f.read())

    # 显示帮助
    def print_help(self):
        # print()
        ColorPrint.get_instance().print_green("     **********  Aiya Client  **********")
        # print()
        ColorPrint.get_instance().print_red("     **郑重声明：本工具仅供内部交流使用，请注意信息安全，由此带来的一切后果与作者无关（正经脸）**")
        # print()
        ColorPrint.get_instance().print_blue("     V" + self._version_)
        print("     功能概述：")
        print("         * cut：文件切分和合并工具，原CutCutCut")
        print("         * send：发送粘贴板数据；数据复制到粘贴板后输入send指令，仅支持文本")
        print("         * get：接收数据到粘贴板；输入get指令后会将接收到的数据复制到粘贴板")
        print()
        print("     Tips：")
        print("     * 粘贴板功能仅支持文本，注意内容不要过多，支持代理")
        # print()
        ColorPrint.get_instance().print_green("     **********  Aiya Client  **********")
        print()

if __name__ == '__main__':
    AiyaClient().main()
    pass
