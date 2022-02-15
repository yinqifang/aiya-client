import os
import configparser
import traceback
from common.config_reader import ConfigReader

# ----- 拆分相关 ----
class SplitConfig:
    section = "split.config"
    def_src_file = "D:\\cutcutcut\\9527.rar"  # 源文件
    def_split_size_in_mb = 25  # 分割大小，25MB

    # 获取源文件值
    def get_src_file(self):
        config_reader = ConfigReader()
        val = config_reader.read_config(config_reader.get_config_file(), self.section, "src.file")
        if not val:
            val = self.def_src_file
        return val

    # 更新源文件值
    def update_src_file(self, src_file):
        config_reader = ConfigReader()
        config_reader.write_config(config_reader.get_config_file(), self.section, "src.file", src_file)

    # 获取分割大小
    def get_split_size(self):
        config_reader = ConfigReader()
        val = config_reader.read_config(config_reader.get_config_file(), self.section, "split.size.in.mb")
        if not val:
            val = self.def_split_size_in_mb
        else:
            val = int(val)
        return val

    # 更新分割大小
    def update_split_size(self, split_size):
        config_reader = ConfigReader()
        config_reader.write_config(config_reader.get_config_file(), self.section, "split.size.in.mb", split_size)


# ----- 邮件相关 ----
class MailConfig:
    section = "mail.config"
    # def_to_address = "fake@mail.com"  # 收件人邮箱列表，分号分割
    def_folder_index = 5  # 接收邮件文件夹，默认5（已发送邮件）
    def_attachment_download_path = "D:\\cutcutcut"  # 邮箱附件保存路径


    # 获取收件人邮箱列表
    def get_to_address(self):
        config_reader = ConfigReader()
        val = config_reader.read_config(config_reader.get_config_file(), self.section, "to.address")
        # if not val:
        #     val = self.def_to_address
        return val

    # 更新收件人邮箱列表
    def update_to_address(self, to_address):
        config_reader = ConfigReader()
        config_reader.write_config(config_reader.get_config_file(), self.section, "to.address", to_address)

    # 获取接收邮件文件夹
    def get_folder_index(self):
        config_reader = ConfigReader()
        val = config_reader.read_config(config_reader.get_config_file(), self.section, "folder.index")
        if not val:
            val = self.def_folder_index
        else:
            val = int(val)
        return val

    # 更新接收邮件文件夹
    def update_folder_index(self, folder_index):
        config_reader = ConfigReader()
        config_reader.write_config(config_reader.get_config_file(), self.section, "folder.index", folder_index)

    # 获取下载路径
    def get_download_path(self):
        config_reader = ConfigReader()
        val = config_reader.read_config(config_reader.get_config_file(), self.section, "attachment.download.path")
        if not val:
            val = self.def_attachment_download_path
        return val

    # 更新下载路径
    def update_download_path(self, download_path):
        config_reader = ConfigReader()
        config_reader.write_config(config_reader.get_config_file(), self.section, "attachment.download.path", download_path)

