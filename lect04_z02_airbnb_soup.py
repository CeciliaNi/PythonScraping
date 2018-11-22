""""
作者：倪媛
功能：用requests及BeautifulSoup来爬取爱彼迎数据
日期：26/10/2018
"""
import requests
from bs4 import BeautifulSoup


def main():
    """
    主函数
    """
    url = 'https://zh.airbnb.com/s/Shenzhen--China/homes?refinement_paths%5B%5D=%2Fhomes&allow_override%5B%5D=&s_tag=-V1Cx7fy&section_offset=5&items_offset=18'

    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.text, 'lxml')

    rent_list = soup.find_all('div', {'class': '_gig1e7'})

    for rent in rent_list:
        print(rent)
        # rent.find


if __name__ == '__main__':
    main()
