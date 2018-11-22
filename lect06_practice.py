"""
作者：倪媛
功能：虎扑论坛帖子数据爬取
日期：04/11/2018
"""
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime
import time


class MongoAPI(object):
    """"
    Mongo的类工具
    """
    def __init__(self, db_ip, db_port, db_name, collection_name):
        self.db_ip = db_ip
        self.db_port = db_port
        self.db_name = db_name
        self.collection_name = collection_name
        # 连接MongoDB 建立客户端
        self.conn = MongoClient(host=self.db_ip, port=self.db_port)
        self.db = self.conn[self.db_name]
        self.collection = self.db[self.collection_name]

    def add(self, kv_dict):
        """
        增加
        """
        return self.collection.insert(kv_dict)

    def check_exist(self, query):
        """
        查询是之前是否有插入过
        """
        ret = self.collection.find_one(query)
        return ret != None

    def update(self, query, kv_dict):
        """
        如果没有就新增
        """
        self.collection.update_one(query, {'$set': kv_dict}, upsert=True)


def get_page(url):
    """
    获取每页soup对象
    """
    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def get_data(tie_list):
    """
    传入每页的帖子列表 获取帖子信息
    """
    post_list = []
    for tie in tie_list:
        # 帖子名称
        tie_name = tie.find_all('div')[0].a.text.strip()
        # 帖子链接
        tie_link = 'https://bbs.hupu.com' + tie.find_all('div')[0].a['href']
        # 作者
        tie_author = tie.find_all('div')[1].a.text.strip()
        # 作者链接
        tie_author_link = tie.find_all('div')[1].a['href']
        # 创建时间
        tie_cre_time = tie.find_all('div')[1].find_all('a')[1].text.strip()
        tie_cre_time = datetime.datetime.strptime(tie_cre_time, '%Y-%m-%d').date()
        # 回复数 浏览数
        tie_comment_num = int(tie.find('span', {'class': 'ansour box'}).text.split('/')[0].strip())
        tie_read_num = int(tie.find('span', {'class': 'ansour box'}).text.split('/')[1].strip())
        # 最后回复用户和最后回复时间
        tie_latest_com_time = tie.find_all('div')[2].a.text.strip()
        if ':' in tie_latest_com_time:
            # 如果只有时和分的时间，将获取当日日期合上
            today_str = str(datetime.date.today())
            tie_latest_com_time = today_str + ' ' + tie_latest_com_time
            tie_latest_com_time = datetime.datetime.strptime(tie_latest_com_time, '%Y-%m-%d %H:%M')
        else:
            tie_latest_com_time = datetime.datetime.strptime(tie_latest_com_time, '%Y-%m-%d').date()
        tie_latest_com_user = tie.find_all('div')[2].span.text.strip()
        # 数据入列表
        data_list = [tie_name, tie_link, tie_author, tie_author_link, tie_cre_time,
                     tie_comment_num, tie_read_num, tie_latest_com_time, tie_latest_com_user]
        # 列表入post列表
        post_list.append(data_list)

    return post_list


def main():
    """
    主函数
    """
    # 爬前十页数据
    for i in range(1, 11):
        url = 'https://bbs.hupu.com/bxj-' + str(i)

        # 调用每页数据爬取函数
        soup = get_page(url)
        # 获取当页的帖子列表
        tie_list = soup.find('ul', {'class': 'for-list'}).find_all('li')
        # 调用参数获得帖子信息
        post_list = get_data(tie_list)

        for post in post_list:
            # 调用MongoDB类工具,建立一个对象
            hupu_post = MongoAPI('localhost', 27017, 'hupu', 'post')
            # 调用类中的更新方法
            hupu_post.update({'tie_link': post[1]},
                          {'tie_name': post[0],
                           'tie_link': post[1],
                           'tie_author': post[2],
                           'tie_author_link': post[3],
                           'tie_cre_time': str(post[4]),
                           'tie_comment_num': post[5],
                           'tie_read_num': post[6],
                           'tie_latest_com_time': str(post[7]),
                           'tie_latest_com_user': post[8]})
        print('第{}行页获取完成，休息3秒'.format(i))
        time.sleep(3)


if __name__ == '__main__':
    main()
