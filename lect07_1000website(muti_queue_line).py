"""
作者：倪媛
功能：使用Queue多线程爬取1000个网页
日期：05/11/2018
"""
import time
import requests
import threading
import queue as Queue

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
    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q

    def run(self):
        print('Starting ', self.name)
        while True:
            try:
                crawler(self.name, self.q)
            except:
                break
        print('Existing ', self.name)


def crawler(threadname, q):
    """
    使用Queue的多线程爬虫
    """
    try:
        url = q.get(timeout=2)
        r = requests.get(url, timeout=20)
        print(q.qsize(), threadname, r.status_code, url)
    except Exception as e:
        print(q.qsize(), threadname, url, 'Error:', e)


def main():
    """
    主函数
    """

    # 起始时间计时
    start_time = time.time()
    print(start_time)

    threadlist = ['thread-1', 'thread-2', 'thread-3', 'thread-4', 'thread-5']
    # 创建一个队列对象,并填充链接网址进去
    workqueue = Queue.Queue(1000)
    for url in web_link_list:
        workqueue.put(url)

    threads = []

    # 创建5个新线程
    for tname in threadlist:
        thread = MyThread(tname, workqueue)
        thread.start()
        threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 结束时间标记
    end_time = time.time()
    print(end_time)

    print('Queue多线程爬虫的总时间为：', end_time - start_time)


if __name__ == '__main__':
    main()
