"""
作者：倪媛
功能：使用multiprocesssing的多进程爬取1000个网页
日期：05/11/2018
"""
import time
import requests
# 在thread多线程中用来控制队列的Queue库，multiprocessing自带了
from multiprocessing import Process, Queue

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


class MyProcess(Process):
    """
    process类
    """
    def __init__(self, q):
        Process.__init__(self)
        self.q = q

    def run(self):
        print('Starting ', self.pid)
        while not self.q.empty():
            crawler(self.q)
        print('Existing ', self.pid)


def crawler(q):
    """
    使用多进程爬虫
    """
    try:
        url = q.get(timeout=2)
        r = requests.get(url, timeout=20)
        print(q.qsize(), r.status_code, url)
    except Exception as e:
        print(q.qsize(), url, 'Error:', e)


def main():
    """
    主函数
    """

    # 起始时间计时
    start_time = time.time()
    print(start_time)

    # 3个进程入进程列表
    # processnames = ['process-1', 'process-2', 'process-3']
    # 创建一个队列对象,并填充链接网址进去
    workqueue = Queue(1000)
    for url in web_link_list:
        workqueue.put(url)

    pros = []

    # 创建3个进程对象
    for i in range(4):
        p = MyProcess(workqueue)
        # 当父进程结束后，子进程就会自动被终止
        p.daemon = True
        p.start()
        pros.append(p)

    for enchopro in pros:
        enchopro.join()

    # 结束时间标记
    end_time = time.time()
    print(end_time)

    print('multiprocessing多进程程爬虫的总时间为：', end_time - start_time)

    print('Main process ended')


if __name__ == '__main__':
    main()
