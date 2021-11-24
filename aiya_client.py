# -*- coding: utf-8 -*-

import requests


def main():
    """
    主流程
    """
    # 登录服务器
    host = '127.0.0.1:8080'
    print("登录服务器：", host)
    # 检查版本号
    # 当前版本
    current_version = 1.0
    # 服务器端最新版本
    latest_version = get_latest_version(host)
    print('检查版本。服务器： %s, 本地： %s' % (latest_version, current_version))


def get_latest_version(host):
    """
    获取最新版本号
    :return:
    """
    url_latest_version = '/aiya/version/latest'
    full_url = "http://" + host + url_latest_version
    resp = requests.get(full_url)
    return resp.text


if __name__ == '__main__':
    main()
