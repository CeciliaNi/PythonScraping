"""
作者：倪媛
功能：使用gevent的多协程爬取1000个网页
日期：06/11/2018
"""
import time
import requests
import gevent
from gevent.queue import Queue, Empty

# 实现爬虫的并发能力
from gevent import monkey           # 把下面有可能有IO操作的单独做上标记
monkey.patch_all()                   # 将IO转为异步执行的函数

# 创建一个队列对象
workqueue = Queue(1000)

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


def crawler(index):
    """
    使用多协程爬虫
    """
    process_id = 'process-'+str(index)

    while not workqueue.empty():
        url = workqueue.get(timeout=2)
        try:
            r = requests.get(url, timeout=20)
            print(process_id, workqueue.qsize(), r.status_code, url)
        except Exception as e:
            print(process_id, workqueue.qsize(), url, 'Error:', e)


def boss():
    """
    填充链接网址进去
    """
    for url in web_link_list:
        workqueue.put(url)


def main():
    """
    主函数
    """
    # 起始时间计时
    start_time = time.time()
    print(start_time)

    # 将队列中加入的内容整合到gevent中
    gevent.spawn(boss).join()

    jobs = []
    # 开发10个协程
    for i in range(10):
        jobs.append(gevent.spawn(crawler, i))

    gevent.joinall(jobs)

    # 结束时间标记
    end_time = time.time()
    print(end_time)

    print('gevent + Queue多协程爬虫的总时间为：', end_time - start_time)

    print('Main ended')


if __name__ == '__main__':
    main()
