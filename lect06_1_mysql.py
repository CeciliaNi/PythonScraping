"""
    作者：倪媛
    功能：将爬取数据存入mysql
    日期：01/11/2018
"""
import requests
from bs4 import BeautifulSoup
import MySQLdb


def main():
    """
    主函数
    """
    # 建立mysql连接
    conn = MySQLdb.connect(host='localhost', user='root',
                           password='3edc#EDC', db='scraping', charset='utf8')
    cur = conn.cursor()

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
        # 用游标将数据写入数据库的url表中
        sql = 'insert into url (url,content) values (\'{}\',\'{}\')'.format(link_url, content)
        cur.execute(sql)

    cur.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
