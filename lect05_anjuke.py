"""
    作者：倪媛
    功能：获取安居客网站上北京二手房的数据
    日期：30/10/2018
"""
import requests
from bs4 import BeautifulSoup


def get_page_data(url):
    # 建立连接
    r = requests.get(url, timeout=30)
    # print(r.status_code)
    soup = BeautifulSoup(r.text, 'lxml')

    # 定位租房信息列表
    house_info_list = soup.find_all('li', {'class': 'list-item'})
    for house_info in house_info_list:
        # 用find
        # house_title = house_info.find('div', {'class': 'house-title'}).a.text.strip()
        # 虽然house-title下有几个div,但是.div选择的是第一个
        house_title = house_info.find('div', {'class': 'house-details'}).div.a.text.strip()
        # 几房几厅
        house_room = house_info.find_all('div', {'class': 'details-item'})[0].find_all('span')[0].text.strip()
        # 大小
        house_size = house_info.find_all('div', {'class': 'details-item'})[0].find_all('span')[1].text.strip()
        # 建造年份
        house_year = house_info.find_all('div', {'class': 'details-item'})[0].find_all('span')[3].text.strip()
        # 联系人
        house_broker = house_info.find_all('div', {'class': 'details-item'})[0].find_all('span')[4].text.strip() \
            .replace('\ue147', '')
        # 价格
        house_price = house_info.find('div', {'class': 'pro-price'}).span.text.strip()
        # 地址  ''.join(str.split())去掉\xa0以及后面的长空格
        house_address = ' '.join(house_info.find_all('div', {'class': 'details-item'})[1].span.text.strip().split())

        # 标签
        house_tag = house_info.find('div', {'class': 'tags-bottom'}).text.strip()

        house_list = [house_title, house_price, house_room, house_size, house_year,
                      house_address, house_tag, house_broker]

        return house_list


def main():
    """
    主函数
    """
    for i in range(1, 21):
        url = 'https://beijing.anjuke.com/sale/p'+str(i)
        house_list = get_page_data(url)

        print(house_list)


if __name__ == '__main__':
    main()
