import os
import random
import shutil
import sys
import tkinter
import traceback
from tkinter import filedialog
from tkinter import messagebox

import colorama

# 添加当前目录到系统路径
# sys.path.append(os.path.dirname(__file__))

from cut_cut_cut.config import SplitConfig
from cut_cut_cut.config import MailConfig
from cut_cut_cut.mail import Mail
from cut_cut_cut.split_and_merge import SplitAndMerge
from cut_cut_cut.zip import Zip
from common.color_print import ColorPrint


class CutCutCut:
    # 定义参数
    _version_ = '1.9'
    _src_file = None
    _file_split_size_in_mb = None
    _mail_to_address = None
    _mail_folder_index = None
    _mail_attachment_download_path = None
    _root_path = None
    _tk_ = None

    # 主流程
    def main(self):
        # 初始化参数
        self.init_variables()
        # 菜单选择
        self.print_menu()
        selected = self.select_menu()
        while selected != "0":
            try:
                if selected == "1":
                    # 发送文件
                    self.send()
                elif selected == "11":
                    # 快捷发送文件（输入文件路径，支持拖入）
                    self.send(fast_model=True, input_file=True, choose_file=False)
                elif selected == "12":
                    # 快捷发送文件（资源管理器中选择文件）
                    self.send(fast_model=True, input_file=False, choose_file=True)
                elif selected == "2":
                    # 接收文件
                    self.receive()
                elif selected == "22":
                    # 快捷接收文件
                    self.fast_receive()
                elif selected == "3":
                    # 清理邮件
                    self.clean_mail()
                elif selected == "33":
                    # 快捷清理邮件
                    self.fast_clean_mail()
                elif selected == "7":
                    # 查看默认参数
                    self.print_config()
                elif selected == "8":
                    # 帮助
                    self.print_help()
                elif selected == "81":
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
        pass

    # 加载默认参数
    def init_variables(self):
        self._root_path = os.getcwd()
        split_config = SplitConfig()
        self._src_file = split_config.get_src_file()
        self._file_split_size_in_mb = split_config.get_split_size()
        # 自动获取邮箱地址
        mail = Mail()
        mail_config = MailConfig()
        self._mail_to_address = mail_config.get_to_address()
        if not self._mail_to_address:
            self._mail_to_address = mail.get_current_account()
        # 自动获取已发送邮件文件夹
        self._mail_folder_index = mail_config.get_folder_index()
        if not self._mail_folder_index:
            self._mail_folder_index = mail.get_sent_box_idx()
        else:
            self._mail_folder_index = int(self._mail_folder_index)

        self._mail_attachment_download_path = mail_config.get_download_path()

        # 初始化窗体
        self._tk_ = tkinter.Tk()
        # 不显示（额外的）主窗体
        self._tk_.withdraw()

    def print_config(self):
        print("原始文件：" + self._src_file)
        print("切分文件大小：" + str(self._file_split_size_in_mb))
        print("收件人地址：" + self._mail_to_address)
        mail = Mail()
        folders = mail.get_mail_folder()
        print("默认搜索文件夹：" + str(self._mail_folder_index) + ", " + folders[self._mail_folder_index])
        print("附件保存路径：" + self._mail_attachment_download_path)
        print("邮箱文件夹： ", end="")
        for key, values in folders.items():
            print(key, values, end="; ")
        print()

    def print_help(self):
        print()
        ColorPrint.get_instance().print_green("     **********  切切切  **********")
        print()
        ColorPrint.get_instance().print_red("     **郑重声明：本工具仅供内部交流使用，请注意信息安全，由此带来的一切后果与作者无关（手动狗头）**")
        print()
        ColorPrint.get_instance().print_blue("     V" + self._version_)
        print("     功能概述：")
        print("         * 发送文件：将文件切分后通过邮件发送给指定收件人")
        print("         * 接收文件：通过取件码自动扫描对应邮件，并将附件合并成原始文件")
        print("         * 清理邮件：清理切切切相关的邮件")
        print("     请确保已经安装Outlook并正确配置了邮件服务器")
        print()
        print("     Tips：")
        print("     * 发送的文件名中不要出现中文")
        print("     * 内网使用时需要以管理员身份运行，否则不能持久化选择的参数")
        print("     * 发送的文件需要再次使用本工具接收，否则无法合并成源文件")
        print()
        ColorPrint.get_instance().print_green("     **********  切切切  **********")
        print()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.environ.get("_MEIPASS2", os.path.dirname(__file__))

        return os.path.join(base_path, relative_path)

    def print_release_notes(self):
        # 获取当前目录
        f = open(self.resource_path("release_notes.txt"), "r", encoding='utf-8')
        print(f.read())

    # 显示菜单
    def print_menu(self):
        print("========== 切切切(V" + self._version_ + ") ==============")
        ColorPrint.get_instance().print_blue("1 . 发送文件")
        ColorPrint.get_instance().print_blue("11. 快捷发送文件（输入文件路径，支持拖入）")
        ColorPrint.get_instance().print_blue("12. 快捷发送文件（资源管理器中选择文件）")
        ColorPrint.get_instance().print_green("2 . 接收文件")
        ColorPrint.get_instance().print_green("22. 快捷接收文件")
        print("3 . 清理邮件")
        print("33. 快捷清理邮件")
        print("7 . 查看默认参数")
        print("8 . 帮助")
        print("81. 更新日志")
        print("9 . 查看菜单")
        ColorPrint.get_instance().print_magenta("0. 退出")

    # 菜单选择
    def select_menu(self):
        return input("请输入要使用的功能（按9菜单，按0退出）：")

    # 发送文件
    def send(self, fast_model=False, input_file=False, choose_file=True):
        """
        发送文件
        :param fast_model: 是否快速模式
        :param input_file: 是否输入文件路径
        :param choose_file: 是否使用资源管理器选择文件
        :return:
        """
        try:
            if fast_model:
                print("单个文件大小限定为: " + str(self._file_split_size_in_mb) + " MB")
                print("接收邮箱: " + self._mail_to_address)
            else:
                # 设置分割大小
                self.config_split_size()
                # 设置接收邮箱
                self.config_mail_to_addr()

            # 设置要发送的文件
            self.config_send_file(input_file=input_file, choose_file=choose_file)

            # 生成取件码
            code = self.gen_magic_code()
            # print("******** 文件提取码: [" + code + "] ********")
            # print()

            # 文件分割
            target_file_path = self.split_files(code)

            # 文件加密，否则发送邮件的时候会触发文件扫描，导致发送很慢
            self.compress_file(code, target_file_path)

            # 邮件发送
            self.send_mail(code, target_file_path)

            # 清理临时文件
            self.clean_send_temp_file(target_file_path)

            # 文本提醒
            print()
            print("****** 文件发送完成，提取码：[", ColorPrint.blue(code), "]，请至接收端接收文件！！！")
            # 弹窗提醒
            self.show_msg_box("CutCutCut", "文件发送完成，提取码：[" + code + "]，请至接收端接收文件。")
            pass
        except Exception as e:
            raise e

    # 设置发送文件
    def config_send_file(self, input_file=False, choose_file=True):
        new_src_file = None
        if input_file:
            # 手动输入文件路径（可以拖动文件到窗口）
            new_src_file = input("请输入要发送文件完整路径[" + self._src_file + "]: ")
        elif choose_file:
            # 使用文件选择器
            init_dir = None
            try:
                init_dir = self.get_path_of_file(self._src_file)
            except Exception:
                pass
            new_src_file = filedialog.askopenfilename(initialdir=init_dir, title="请选择需要发送的文件")
            self._src_file = None

        if new_src_file and new_src_file.strip():
            self._src_file = new_src_file
            # 更新配置文件
            split_config = SplitConfig()
            split_config.update_src_file(self._src_file)
            print("发送文件修改为: " + self._src_file)

        # if not self._src_file:
        #     print("请选择要发送的文件！")
        #     raise Exception("没有找到需要发送的文件！")
        if not os.path.exists(self._src_file):
            print("文件[" + self._src_file + "]不存在！")
            raise Exception("文件[" + self._src_file + "]不存在！")

    # 设置分割大小
    def config_split_size(self):
        new_split_size_in_mb = input("请输入单个文件大小，单位MB[" + str(self._file_split_size_in_mb) + "MB]: ")
        if new_split_size_in_mb and new_split_size_in_mb.strip():
            self._file_split_size_in_mb = int(new_split_size_in_mb)
            # 更新配置文件
            split_config = SplitConfig()
            split_config.update_split_size(self._file_split_size_in_mb)
            print("单个文件大小限定为: " + str(self._file_split_size_in_mb) + " MB")

    # 设置接收邮箱
    def config_mail_to_addr(self):
        new_mail_to_addr = input("请输入接收邮箱[" + self._mail_to_address + "]: ")
        if new_mail_to_addr and new_mail_to_addr.strip():
            self._mail_to_address = new_mail_to_addr
            # 更新配置文件
            mail_config = MailConfig()
            mail_config.update_to_address(self._mail_to_address)
            print("接收邮箱修改为: " + self._mail_to_address)

    # 分割文件， 返回分割后的临时目录名称
    def split_files(self, code):
        prompt = "分割文件(" + self._src_file + ", " + str(self._file_split_size_in_mb) + "MB)..."
        self.progress_start(prompt)
        try:
            src_file_path = os.path.dirname(self._src_file)
            target_file_path = os.path.join(src_file_path, code)
            if not os.path.exists(target_file_path):
                os.makedirs(target_file_path)
            # 判断是否需要拆分
            file_size_in_mb = os.path.getsize(self._src_file) / float(1024 * 1024)
            if file_size_in_mb <= self._file_split_size_in_mb:
                # 未超过切分大小，不需要分割，原样拷贝
                print()
                print("文件大小(%fMB)未超过限制(%fMB)，不分割。" % (file_size_in_mb, self._file_split_size_in_mb))
                shutil.copy(self._src_file, target_file_path)
            else:
                split_and_merge = SplitAndMerge()
                split_and_merge.split(srcFileName=self._src_file, tarFilePath=target_file_path,
                                      splitSize=self._file_split_size_in_mb * 1024 * 1024)
        except Exception as e:
            self.progress_error(prompt)
            print(traceback.format_exc())
            raise e
        else:
            self.progress_succeed(prompt)

        return target_file_path

    # 加密文件
    def compress_file(self, code, target_file_path):
        prompt = "加密文件..."
        self.progress_start(prompt)
        try:
            zip = Zip()
            for root, dirs, files in os.walk(target_file_path):
                idx = 0
                for filename in files:
                    idx += 1
                    zip.compress(os.path.join(target_file_path, filename),
                                 os.path.join(target_file_path, filename + ".rar"),
                                 code, True)
                    self.progress_ing(prompt, idx, len(files))
        except Exception as e:
            self.progress_error(prompt)
            print(traceback.format_exc())
            raise e
        else:
            self.progress_succeed(prompt, idx, len(files))

    # 发送邮件
    def send_mail(self, code, target_file_path):
        prompt = "发送邮件..."
        self.progress_start(prompt)
        try:
            mail = Mail()
            for root, dirs, files in os.walk(target_file_path):
                idx = 0
                for filename in files:
                    idx += 1
                    subject = "[CutCutCut][" + code + "]-" + str(len(files)) + "-" + str(idx)
                    body = filename
                    attachments = [os.path.join(target_file_path, filename)]
                    self.progress_ing(prompt, idx, len(files))
                    # print("Sending " + ",".join(attachments))
                    mail.send(to=self._mail_to_address, subject=subject, body=body, attachments=attachments)
                    # time.sleep(5)
        except Exception as e:
            self.progress_error(prompt)
            print(traceback.format_exc())
            raise e
        else:
            self.progress_succeed(prompt, idx, len(files))

    # 清理发送时临时文件
    def clean_send_temp_file(self, target_file_path):
        prompt = "清理临时文件..."
        self.progress_start(prompt)
        try:
            shutil.rmtree(target_file_path)
        except Exception as e:
            self.progress_error(prompt)
            print(traceback.format_exc())
            raise e
        else:
            self.progress_succeed(prompt)

    # 接收文件
    def receive(self):
        try:
            # 设置搜索邮件文件夹
            self.config_search_folder()

            # 输入提取码
            magic_code = self.config_magic_code()

            # 设置文件下载路径
            self.config_download_path()

            # 下载附件
            tar_path = self.download_attachment(magic_code)

            # 解压文件
            split_files = self.uncompress_file(magic_code, tar_path)

            # 拼接文件
            self.merge_file(split_files, tar_path)

            # 清理临时文件
            self.clean_receive_temp_file(split_files)

            print("****** 文件合并成功！！！目标文件夹：", ColorPrint.blue(tar_path))

            # 打开目标文件夹
            os.startfile(tar_path)
        except Exception as e:
            raise e

    # 快捷接收文件
    def fast_receive(self):
        try:
            mail = Mail()
            folders = mail.get_mail_folder()
            print("搜索邮箱文件夹: " + str(self._mail_folder_index) + ", " + folders[self._mail_folder_index])
            print("文件下载路径: " + self._mail_attachment_download_path)
            # 输入提取码
            magic_code = self.config_magic_code()

            # 下载附件
            tar_path = self.download_attachment(magic_code)

            # 解压文件
            split_files = self.uncompress_file(magic_code, tar_path)

            # 拼接文件
            self.merge_file(split_files, tar_path)

            # 清理临时文件
            self.clean_receive_temp_file(split_files)

            print("****** 文件合并成功！！！目标文件夹：", ColorPrint.blue(tar_path))

            # 打开目标文件夹
            os.startfile(tar_path)
        except Exception as e:
            raise e

    # 设置搜索文件夹
    def config_search_folder(self):
        mail = Mail()
        folders = mail.get_mail_folder()
        sent_box_idx = mail.get_sent_box_idx()
        in_box_idx = mail.get_in_box_idx()
        choose_folder_tips = "请输入要搜索的邮箱文件夹，" + str(sent_box_idx) + "：已发送邮件， " + str(in_box_idx) + "：收件箱[" + str(
            self._mail_folder_index) + "]: "
        new_folder_index = input(choose_folder_tips)
        if new_folder_index and new_folder_index.strip():
            self._mail_folder_index = int(new_folder_index)
            # 更新配置文件
            mail_config = MailConfig()
            mail_config.update_folder_index(self._mail_folder_index)
            print("搜索邮箱文件夹修改为: " + str(self._mail_folder_index) + ", " + folders[self._mail_folder_index])

    # 设置提取码
    def config_magic_code(self):
        magic_code = self.get_magic_code(self._mail_folder_index)
        new_magic_code = input("请输入提取码[" + str(magic_code or '') + "]: ")
        if new_magic_code and new_magic_code.strip():
            print("取件码: " + new_magic_code)
            magic_code = new_magic_code
        if not magic_code:
            print("取件码为空！")
            raise Exception("取件码为空")
        return magic_code

    # 设置文件下载路径
    def config_download_path(self):
        # # 手动输入下载路径
        # new_mail_attachment_download_path = input("请输入附件下载路径[" + self._mail_attachment_download_path + "]: ")
        # 使用文件夹选择器
        new_mail_attachment_download_path = filedialog.askdirectory(initialdir=self._mail_attachment_download_path,
                                                                    title="请选择附件下载路径")
        if new_mail_attachment_download_path and new_mail_attachment_download_path.strip():
            self._mail_attachment_download_path = new_mail_attachment_download_path
            # 更新配置文件
            mail_config = MailConfig()
            mail_config.update_download_path(self._mail_attachment_download_path)
            print("文件下载路径修改为: " + self._mail_attachment_download_path)

    # 下载附件
    def download_attachment(self, magic_code):
        prompt = "下载附件..."
        self.progress_start(prompt)
        try:
            mail = Mail()
            filter_subject = "[CutCutCut][" + magic_code + "]"
            qualified_mails = mail.filter_mails_from_folder(filter_subject, self._mail_folder_index, 100)
            # 检查是否有邮件
            if len(qualified_mails) <= 0:
                self.progress_error(prompt, "--未找到对应邮件，请确保取件码正确并且邮件已发送成功！！！")
                raise Exception("--未找到对应邮件，请确保取件码正确并且邮件已发送成功！！！")
            # 检查邮件数量是否正确
            subject = qualified_mails[0].Subject
            split_subject = subject.split("-")
            if len(split_subject) >= 3:
                total_mail_count = int(split_subject[len(split_subject) - 2])
                if len(qualified_mails) < total_mail_count:
                    # 邮件数量不够
                    self.progress_custom(prompt, ColorPrint.red("--邮件数量不正确，期望："), ColorPrint.cyan(str(total_mail_count)),
                                         ColorPrint.red("， 实际："), ColorPrint.magenta(str(len(qualified_mails))))
                    print()
                    for mail in qualified_mails:
                        print("    --", mail.Subject)
                    raise Exception("邮件数量不正确")
            self.progress_custom(prompt, "扫描到 ", ColorPrint.cyan(str(len(qualified_mails))), " 封邮件，开始下载")
            print()
            tar_path = os.path.join(self._mail_attachment_download_path, magic_code)
            mail.fetch_attachment(qualified_mails, tar_path)
        except Exception as e:
            self.progress_error(prompt)
            print(traceback.format_exc())
            raise e
        else:
            self.progress_succeed(prompt)
        # 返回下载目录
        return tar_path

    # 解压文件，返回解压后的文件集合
    def uncompress_file(self, magic_code, tar_path):
        prompt = "解密文件..."
        self.progress_start(prompt)
        try:
            zip = Zip()
            for root, dirs, files in os.walk(tar_path):
                idx = 0
                for filename in files:
                    idx += 1
                    zip.uncompress(os.path.join(tar_path, filename), magic_code, tar_path, True)
                    self.progress_ing(prompt, idx, len(files))
        except Exception as e:
            self.progress_error(prompt)
            print(traceback.format_exc())
            raise e
        else:
            self.progress_succeed(prompt)
        # 记录原始文件，用于后续的清理
        split_files = None
        for root, dirs, files in os.walk(tar_path):
            split_files = files
        return split_files

    # 拼接文件
    def merge_file(self, split_files, tar_path):
        prompt = "拼接文件..."
        self.progress_start(prompt)
        try:
            # 判断是否需要拼接
            file_number = len(split_files)
            if file_number <= 1:
                # 不需要拼接
                pass
            else:
                # 需要拼接
                merge = SplitAndMerge()
                merge.merge(tar_path)
        except Exception as e:
            self.progress_error(prompt)
            print(traceback.format_exc())
            raise e
        else:
            self.progress_succeed(prompt)

    # 清理接收时临时文件
    def clean_receive_temp_file(self, split_files):
        prompt = "清理临时文件..."
        self.progress_start(prompt)
        try:
            file_number = len(split_files)
            if file_number <= 1:
                # 不需要清理，没有临时文件
                pass
            else:
                for split_file in split_files:
                    os.remove(split_file)
        except Exception as e:
            self.progress_error(prompt)
            print(traceback.format_exc())
            raise e
        else:
            self.progress_succeed(prompt)

    # 获取邮箱文件夹中第一封匹配邮件的取件码
    def get_magic_code(self, mail_folder_index):
        mail = Mail()
        mails = mail.filter_mails_from_folder("[CutCutCut]", mail_folder_index, 1)
        if len(mails) <= 0:
            return None
        subject = mails[0].Subject
        start_idx = subject.index("[CutCutCut]")
        return subject[start_idx + 12:start_idx + 16]

    # 清理邮件
    def clean_mail(self):
        # 设置提取码，删除前需要确认
        search_code = input("请输入要清理的提取码: ")
        self.clean_mail_with_full_params(search_code, True)

    # 快捷清理邮件
    def fast_clean_mail(self):
        # 全部删除，删除前不需要确认
        self.clean_mail_with_full_params("", False)

    # 清理邮件（完整参数）
    def clean_mail_with_full_params(self, search_code, confirm_before_delete):
        # 设置提取码，拼装搜索主题
        search_subject = "[CutCutCut]"
        if search_code and search_code.strip():
            search_subject += "[" + search_code + "]"
        # 获取所有邮箱文件夹
        mail = Mail()
        mail_folder_index_vs_name = mail.get_mail_folder()
        # 搜索邮件
        mail_folder_name_vs_mails = {}
        max_search_count = 50  # 每个文件夹最多搜索前50封邮件
        for idx, name in mail_folder_index_vs_name.items():
            # # 忽略已删除文件夹
            # if "已删除" in name:
            #     continue
            mails = mail.filter_mails_from_folder(search_subject, idx, max_search_count)
            if len(mails) <= 0:
                continue
            if "已删除" in name:
                # 扫描到已删除文件夹中内容，删除前需要确认
                confirm_before_delete = True
            mail_folder_name_vs_mails[name] = mails
        # 展示扫描结果
        if len(mail_folder_name_vs_mails) <= 0:
            ColorPrint.get_instance().print_green("没有找到待清理的邮件！")
            return
        else:
            ColorPrint.get_instance().print_green("扫描到如下邮件：")
            for folder_name, mails in mail_folder_name_vs_mails.items():
                ColorPrint.get_instance().print_cyan("++" + folder_name + "(" + str(len(mails)) + ")")
                for mail in mails:
                    ColorPrint.get_instance().print_magenta("  --" + mail.Subject)
        # 确认是否删除
        if confirm_before_delete:
            confirm_delete = input("是否删除所有扫描到的邮件，已删除中邮件会被彻底删除且无法恢复！！[y/n]：")
            if confirm_delete != "y":
                print(ColorPrint.yellow("放弃清理"))
                return
        # 删除
        prompt = "清理邮件..."
        self.progress_start(prompt)
        for folder_name, mails in mail_folder_name_vs_mails.items():
            prompt = "清理邮件[" + folder_name + "]..."
            self.progress_start(prompt)
            idx = 0
            for mail in mails:
                idx += 1
                mail.Delete()
                self.progress_ing(prompt, idx, len(mails))
            self.progress_succeed(prompt, idx, len(mails))

    # 生成取件码
    def gen_magic_code(self):
        code = ""
        for i in range(4):
            code += str(random.randint(0, 9))
        return code
        pass

    def progress_start(self, prompt):
        print("\r", prompt, end="")

    def progress_ing(self, prompt, current, total):
        # red, green, yellow, blue, magenta, cyan, white.
        print("\r", prompt, ColorPrint.magenta(str(current)), "/", ColorPrint.cyan(str(total)), end="")

    def progress_error(self, prompt, err_msg="失败!!!"):
        print("\r", prompt, ColorPrint.red(err_msg), end="")
        print()

    def progress_succeed(self, prompt, current=None, total=None):
        if current == None:
            print("\r", prompt, ColorPrint.green("Done！"), end="")
        else:
            print("\r", prompt, ColorPrint.magenta(str(current)), "/", ColorPrint.cyan(str(total)),
                  ColorPrint.green("Done！"), end="")
        print()

    def progress_custom(self, *args):
        prompt = ""
        for arg in args:
            prompt += arg
        print("\r", prompt, end="")

    def show_msg_box(self, title, msg, top=True):
        # 设置是否置顶
        self._tk_.wm_attributes('-topmost', top)
        # 弹窗
        messagebox.showinfo(title, msg)
        pass

    # 获取文件所属的文件夹路径
    def get_path_of_file(self, full_file_name):
        (file_path, file_name) = os.path.split(full_file_name)
        return file_path


if __name__ == '__main__':
    colorama.init()
    pass
    # print(os.path.dirname("d:\\cutcutcut\\9527.rar"))
    CutCutCut().main()
    # testSplit()
    # testMerge()
