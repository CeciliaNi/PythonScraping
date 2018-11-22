"""
作者：倪媛
功能：TOR浏览器更换IP
日期：13/11/2018
"""
from stem import Signal
from stem.control import Controller
import socket
import socks
import requests
import time


def main():
    """
    主函数
    """
    controller = Controller.from_port(port=9151)
    controller.authenticate()
    # Tor使用9150端口为默认的socks端口
    socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9150)
    socket.socket = socks.socksocket

    total_scrappy_time = 0
    total_changeip_time = 0

    for i in range(10):
        # 获取这次抓取使用的IP地址
        a = requests.get('http://checkip.amazonaws.com').text
        print('第{}次IP:{}'.format(i+1, a))

        # 计算每次的抓取时间
        time1 = time.time()
        a = requests.get('https://www.baidu.com', timeout=30).text
        time2 = time.time()
        total_scrappy_time = total_scrappy_time + time2 - time1
        print('第{}次抓取时间:{}'.format(i+1, time2 - time1))

        # 计算更换IP的时间
        time3 = time.time()
        controller.signal(Signal.NEWNYM)
        time.sleep(5)
        time4 = time.time()
        total_changeip_time = total_changeip_time + time4 - time3
        print('第{}次更换IP花费时间:{}'.format(i + 1, time4 - time3 - 5))

    print('平均抓取花费时间：', total_scrappy_time/10)
    print('平均更换IP花费时间：', total_changeip_time / 10)


if __name__ == '__main__':
    main()
