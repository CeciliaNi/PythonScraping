"""
    作者：倪媛
    功能：将爬取数据存入mongodb
    日期：03/11/2018
"""
import requests
import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient


def main():
    """
    主函数
    """
    # 建立MongoDB客户端
    client = MongoClient('localhost', 27017)
    # 连接blog_database,如果没有该数据库将会创建一个数据库
    db = client.blog_database
    # 选择blog_database数据库下的blog集合，如果没有将会创建一个
    collection = db.blog

    # 建立网址连接
    url = 'http://www.santostang.com/'
    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.text, 'lxml')
    # 找到所有标题的列表
    link_list = soup.find_all('h1', {'class': 'post-title'})
    for link in link_list:
        # 获取链接
        link_url = link.a['href']
        # 获取标题
        content = link.a.text.strip()

        post = {'url': link_url,
                'title': content,
                'date': datetime.datetime.utcnow()}
        collection.insert_one(post)


if __name__ == '__main__':
    main()
