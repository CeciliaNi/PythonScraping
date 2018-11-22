"""
    作者：倪媛
    功能：抓取TOP250电影数据
    日期：22/10/2018
"""
import requests
from bs4 import BeautifulSoup


def main():
    """
    主函数
    """
    for i in range(10):
        # 将url的start=部分循环加25来实现网页的变化
        url = 'https://movie.douban.com/top250?start=' + str(25*i)
        # 建立连接
        r = requests.get(url, timeout=30)
        # 把HTML代码转化成soup对象
        soup = BeautifulSoup(r.text, 'lxml')
        # 找到标题行列表
        title_list = soup.find_all('div', {'class': 'hd'})
        # 循环每个元素找到具体的标题
        for title in title_list:
            # 只返回找到元素的第一个标签
            # title_name = title.a.span.text.strip()
            title_name = title.find('span', {'class': 'title'}).text.strip()
            print(title_name)


if __name__ == '__main__':
    main()
