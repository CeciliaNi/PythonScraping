"""
作者：倪媛
功能：TOR浏览器的使用
日期：13/11/2018
"""
import socket
import socks
import requests


def main():
    """
    主函数
    """
    # Tor使用9150端口为默认的socks端口
    socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9150)
    socket.socket = socks.socksocket
    # 获取这次抓取使用的IP地址
    a = requests.get('http://checkip.amazonaws.com').text

    print(a)


if __name__ == '__main__':
    main()
