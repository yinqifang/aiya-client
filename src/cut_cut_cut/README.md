# 说明
文件传输助手
## 操作
### 发送端
1. 文件切分，防止超过单邮件附件限制
2. 文件加密，防止发送时触发文件扫描导致发送变慢
3. 生成文件提取码
4. 邮件发送，主题增加关键字
### 接收端
1. 通过提取码获取对应邮件
2. 附件提取
3. 文件解密
4. 文件合并
### python转exe
~~~
pip install pyinstaller
python -m PyInstaller CutCutCut.spec
~~~
## 参考文档
* [Outlook Item属性](https://docs.microsoft.com/zh-cn/office/vba/api/outlook.mailitem)
* [文件选择器](https://blog.csdn.net/SL_World/article/details/96920390)