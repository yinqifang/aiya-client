import sys
import os


class Resource:

    # 用于处理PyInstaller打包后的程序访问资源文件路径问题
    @staticmethod
    def resource_path(file_name, default_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.environ.get("_MEIPASS2", default_path)

        return os.path.join(base_path, file_name)
