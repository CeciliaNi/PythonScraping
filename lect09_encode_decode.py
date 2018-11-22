"""
作者：倪媛
功能：解决中文乱码的问题
日期：07/11/2018
"""
import requests
from bs4 import BeautifulSoup


def main():
    """
    主函数
    """
    # url = 'http://w3school.com.cn/'
    # r = requests.get(url, timeout=20)
    # # 网页的响应体r的编码格式是ISO-88591,而网页真正使用的编码是gbk,所以要统一编码
    # r.encoding = 'gbk'
    # soup = BeautifulSoup(r.text, 'lxml')
    #
    # txt = soup.find('div', {'class': 'idea'}).text.strip()
    # print(txt)

    url2 = 'http://www.sina.com.cn/'
    r = requests.get(url2, timeout=20)
    r.encoding = 'utf-8'
    soup2 = BeautifulSoup(r.text, 'lxml')

    li_list = soup2.find('ul', {'class': 'list-a news_top'}).find_all('li')

    for li in li_list:
        print(li.text.strip())


if __name__ == '__main__':
    main()
