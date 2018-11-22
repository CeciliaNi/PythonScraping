"""
作者：倪媛
功能：爬取知乎live的相关数据
日期：19/11/2018
"""
import requests
import json
from pymongo import MongoClient
import time
import random


# 建立MongoDB客户端
client = MongoClient('localhost', 27017)
# 连接zhihu_database,如果没有该数据库将会创建一个数据库
db = client.zhihu_database
# 选择zhihu_database数据库下的live集合，如果没有将会创建一个
collection = db.live


def get_audience(url, live_id):
    """
    获取每个live的观众
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36'}

    r = requests.get(url, headers=headers)

    decodejson = json.loads(r.text)
    # 增加一个live_id的数据
    decodejson['live_id'] = live_id
    next_page = decodejson['paging']['next']
    is_end = decodejson['paging']['is_end']

    # 插入mongodb数据库中
    db.live_audience.insert_one(decodejson)

    return next_page, is_end


def scrapy(url):
    """
    爬取函数
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36'}

    r = requests.get(url, headers=headers)
    html = r.text

    # 注意这里是loads不是load,load加载的是文件
    decodejson = json.loads(html)
    # 将json数据插入到MongoDB中
    collection.insert_one(decodejson)

    # 获取下一页链接及是否结束标志
    next_page = decodejson['paging']['next']
    is_end = decodejson['paging']['is_end']

    return next_page, is_end


def main():
    """
    主函数
    """

    url = 'https://api.zhihu.com/lives/homefeed?includes=live'

    # 调用爬取函数
    next_page, is_end = scrapy(url)
    # 循环调用爬取函数 获得所有的live课题集合
    while not is_end:
        next_page, is_end = scrapy(next_page)

    # 循环live这个集合
    for ench_page in collection.find():
        for ench in ench_page['data']:
            # 获取liveid 以供下面获取观众列表
            live_id = ench['live']['id']

            # 接下来进行观众列表的获取
            url = 'https://api.zhihu.com/lives/' + live_id + '/members'
            next_page, is_end = get_audience(url, live_id)
            # 判断是否结束 如未结束再次进行循环
            while not is_end:
                next_page, is_end = get_audience(next_page, live_id)
                # 设置随机等待一段时间
                time.sleep(random.randint(3, 4) + random.random())


if __name__ == '__main__':
    main()
