"""
作者：倪媛
功能：使用pool+queue的多进程爬取1000个网页
日期：06/11/2018
"""
import time
import requests
from multiprocessing import Pool, Manager

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


def crawler(q, index):
    """
    使用多进程爬虫
    """
    process_id = 'process-'+str(index)

    while not q.empty():
        url = q.get(timeout=2)
        try:
            r = requests.get(url, timeout=20)
            print(process_id, q.qsize(), r.status_code, url)
        except Exception as e:
            print(process_id, q.qsize(), url, 'Error:', e)


def main():
    """
    主函数
    """

    # 起始时间计时
    start_time = time.time()
    print(start_time)

    manger = Manager()
    # 创建一个队列对象,并填充链接网址进去
    workqueue = manger.Queue(1000)
    for url in web_link_list:
        workqueue.put(url)

    # 创建进程池，设置创建进程的最大值为3
    pool = Pool(processes=3)
    # 使用pool创建4个子进程
    for i in range(4):
        # 创建非阻塞进程
        pool.apply_async(crawler, args=(workqueue, i))

    print('started processes')
    pool.close()
    pool.join()

    # 结束时间标记
    end_time = time.time()
    print(end_time)

    print('pool + Queue多进程爬虫的总时间为：', end_time - start_time)

    print('Main process ended')


if __name__ == '__main__':
    main()
