"""
作者：倪媛
功能：简单的threading多线程爬取1000个网页
日期：05/11/2018
"""
import time
import requests
import threading

# 获取文件中的网页列表,是一个全局变量
with open('alexa.txt', mode='r') as f:
    # 获取网页列表
    website_list = f.readlines()
    # 循环读取网页列表
    web_link_list = []
    for website in website_list:
        web_link = website.split('\t')[1]
        web_link = web_link.replace('\n', '')
        web_link_list.append(web_link)


class MyThread(threading.Thread):
    """
    Thread类
    """
    def __init__(self, name, link_range):
        threading.Thread.__init__(self)
        self.name = name
        self.link_range = link_range

    def run(self):
        print('Starting ', self.name)
        crawler(self.name, self.link_range)
        print('Existing ', self.name)


def crawler(threadname, link_range):
    """
    分链接区间来进行爬虫
    """
    for i in range(link_range[0], link_range[1]+1):
        try:
            r = requests.get(web_link_list[i], timeout=20)
            print(threadname, r.status_code, web_link_list[i])
        except Exception as e:
            print(threadname, 'Error', e)


def main():
    """
    主函数
    """

    # 起始时间计时
    start_time = time.time()
    print(start_time)

    thread_list = []
    link_range_list = [(0, 200), (201, 400), (401, 600), (601, 800), (801, 1000)]

    # 创建5个新线程
    for i in range(1, 6):
        thread = MyThread('Thread-'+str(i), link_range_list[i-1])
        thread.start()
        thread_list.append(thread)

    # 等待所有线程完成
    for thread in thread_list:
        thread.join()
    # 结束时间标记
    end_time = time.time()
    print(end_time)

    print('串行的总时间为：', end_time - start_time)


if __name__ == '__main__':
    main()
