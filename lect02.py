"""
    作者：倪媛
    功能：爬取santostang博客的文章标题
"""
import requests
from bs4 import BeautifulSoup
import csv


def main():
    """
    主函数
    """
    # 建立连接
    url = 'http://www.santostang.com/'
    r = requests.get(url, timeout=30)
    # 把HTML代码转化成soup对象
    soup = BeautifulSoup(r.text, 'lxml')
    # 找到h1标签
    h1_list = soup.find_all('h1', {'class': 'post-title'})

    # 将每个标签的文本输出

    with open('title.csv', mode='w', encoding='utf-8', newline='')as f:
        header = ['title']
        writer = csv.writer(f)
        writer.writerow(header)
        for h1 in h1_list:
            text_title = h1.text.strip()
            row = [text_title]
            writer.writerow(row)


if __name__ == '__main__':
    main()
