from common.color_print import ColorPrint
from cut_cut_cut.cut_cut_cut import CutCutCut

class AiyaClient:
    # 定义参数
    _version_ = '1.0'

    # 主流程
    def main(self):
        print("欢迎使用哎呀(V" + self._version_ + ")")
        ColorPrint.get_instance().print_red("本工具仅供内部研究使用，请注意信息安全，由此带来的一切后果与作者无关（手动狗头）")

        # 打印CutCutCut菜单
        CutCutCut().main()


if __name__ == '__main__':
    AiyaClient().main()
    pass
