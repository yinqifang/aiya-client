import os

import win32com.client as win32


# toAddress = 'to@mail.com'  # 收件人邮箱列表，分号分割
# attachmengDownloadPath = "D:\\cutcutcut"  # 邮箱附件保存地址
class Mail:
    # 发送邮件
    def send(self, to, subject, body, attachments):
        outlook = win32.Dispatch("outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = to
        mail.Subject = subject
        for attachment in attachments:
            mail.Attachments.Add(attachment)
        mail.Body = body
        mail.Send()
        # print(str(datetime.datetime.now()) + ": 6")
        # print("Send mail succeed! Subject: " + subject)
        # outlook.Application.Quit()
        # print(str(datetime.datetime.now()) + ": 7")

    # 获取邮箱目录和序号，仅返回和邮件相关的目录
    def get_mail_folder(self):
        outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
        folders = {}
        for i in range(10):
            try:
                box = outlook.GetDefaultFolder(i)
                # 邮件文件夹类型值为0，https://docs.microsoft.com/zh-cn/office/vba/api/outlook.olitemtype
                if box.DefaultItemType != 0:
                    # print(box.Name, " 不是邮件文件夹")
                    continue
                name = box.Name
                folders[i] = name
            except:
                pass
        return folders
        # outlook.Application.Quit()

    # 打印邮箱目录和序号
    def print_mail_folder(self):
        folders = self.get_mail_folder()
        for key, values in folders.items():
            print(key, values)
        # outlook.Application.Quit()

    # 打印邮箱目录和序号
    def print_mail_folder_in_one_line(self):
        folders = self.get_mail_folder()
        for key, values in folders.items():
            print(key, values, end="; ")
        print()
        # outlook.Application.Quit()

    # 获取已发送邮件文件夹索引
    def get_sent_box_idx(self):
        folders = self.get_mail_folder()
        for key, values in folders.items():
            if "已发送邮件" in values:
                return key
        print("未找到已发送邮件文件夹")

    # 获取收件箱文件夹索引
    def get_in_box_idx(self):
        folders = self.get_mail_folder()
        for key, values in folders.items():
            if "收件箱" in values:
                return key
        print("未找到收件箱文件夹")

    # 获取当前用户邮箱地址
    def get_current_account(self):
        outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
        send_box_idx = self.get_sent_box_idx()
        if not send_box_idx:
            return
        sentBox = outlook.GetDefaultFolder(send_box_idx)
        if len(sentBox.Items) <= 0:
            return None
        mailItem = sentBox.Items[0]
        currentAccount = ""
        if mailItem.SenderEmailType == "EX":
            currentAccount = mailItem.Sender.GetExchangeUser().PrimarySmtpAddress
        else:
            currentAccount = mailItem.SenderEmailAddress
        # outlook.Application.Quit()
        return currentAccount

    # 从文件夹索引中过滤邮件（4:发件箱; 5:已发送邮件; 6:收件箱），支持子文件夹
    def filter_mails_from_folder(self, filter_subject, folder_idx, max_search_count):
        # 获取邮件目录
        outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
        mail_folder = outlook.GetDefaultFolder(folder_idx)
        # 递归获取所有邮件
        qualified_mails = self.filter_mails_from_folder_obj(filter_subject, mail_folder, max_search_count)
        
        return qualified_mails

    # 从文件夹对象中过滤邮件
    def filter_mails_from_folder_obj(self, filter_subject, folder_obj, max_search_count):
        qualified_mails = []
        # 添加根目录邮件
        root_items = folder_obj.Items
        root_mails = self.filter_mails_from_items(filter_subject, root_items, max_search_count)
        qualified_mails.extend(root_mails)
        # 添加子文件夹邮件
        sub_folders = folder_obj.Folders
        for sub_folder in sub_folders:
            sub_mails = self.filter_mails_from_folder_obj(filter_subject, sub_folder, max_search_count)
            qualified_mails.extend(sub_mails)

        return qualified_mails

    # 从Items对象中过滤邮件(https://docs.microsoft.com/en-us/office/vba/api/outlook.items)
    def filter_mails_from_items(self, filter_subject, items, max_search_count):
        qualified_mails = []
        if len(items) <= 0:
            return qualified_mails
        # 将邮件按接收时间排序
        items.Sort("[ReceivedTime]", True)
        # 最多查询最近max_search_count封邮件
        if max_search_count > len(items):
            max_search_count = len(items)
        for i in range(max_search_count):
            mail = items[i]
            subject = mail.Subject
            if filter_subject not in subject:
                continue
            qualified_mails.append(mail)
        return qualified_mails

    # 提取邮件中附件
    def fetch_attachment(self, mails, download_path):
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        for mail in mails:
            attachments = mail.attachments
            for attachment in attachments:
                targetFile = os.path.join(download_path, attachment.FileName)
                # print("Got " + attachment.FileName + " from mail [" + mail.Subject + "] ==> " + targetFile)
                attachment.SaveASFile(targetFile)
                pass
        # outlook.Application.Quit()
        return download_path


if __name__ == '__main__':
    pass
    Mail().print_mail_folder()
    # Mail().print_mail_folder_in_one_line()
    # fetchAttachmentFromSentBox("abc")
    # print(Mail().get_sent_box_idx())
    # print(Mail().get_in_box_idx())
    # print(Mail().get_current_account())

    # # 测试子文件邮件搜索
    # mails = Mail().filter_mails_from_folder("[CutCutCut][2045]", 6, 20)
    # for mail in mails:
    #     print(mail.Subject)

    # outlook = win32.Dispatch("Outlook.Application")
    # namespace = outlook.GetNamespace("MAPI")
    # folder = namespace.GetDefaultFolder(6)
    # print(folder.DefaultItemType)
    # print(win32.constants)
    # print(win32.constants.olFolderInbox)
    # print(win32.constants.OlItemType)
    # for const in win32.constants:
    #     print(const)
