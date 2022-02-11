import pyperclip


class Clipboard:

    @staticmethod
    # 从粘贴板获取数据
    def get_data_from_clipboard():
        return pyperclip.paste()

    # 数据写入到粘贴板
    @staticmethod
    def write_data_to_clipboard(data):
        pyperclip.copy(data)
        # pyperclip.paste()
