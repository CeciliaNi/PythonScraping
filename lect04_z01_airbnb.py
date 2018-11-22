""""
    作者：倪媛
    功能：爬取爱彼迎深圳地区前20页租房信息
    日期：24/10/2018
"""
from selenium import webdriver
import time


# def get_page_data():


def main():
    """
    主函数
    """
    # get_page_data()
    # 设置chorme选项
    chrome_options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values':
        {
            'images': 2
            # ,
            # 'javascript': 2
        }
    }
    chrome_options.add_experimental_option('prefs', prefs)
    # for i in range(1):
    url = 'https://zh.airbnb.com/s/Shenzhen--China/homes?items_offset=0' + str(i * 18)
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # driver = webdriver.Chrome()
    # 设置最大等待时间
    driver.implicitly_wait(20)
    driver.get(url)

    # 打开地图模式
    driver.maximize_window()
    # driver.find_element_by_id('MapToggleBar').click()

    # 获取租房列表
    rent_list = driver.find_elements_by_css_selector('div._gig1e7')
    # print(rent_list)

    for rent in rent_list:
        # name = rent.find_element_by_tag_name('meta').get_attribute('content')
        name = rent.find_element_by_css_selector('div._spquhs7').text.strip()
        price = rent.find_elements_by_css_selector('span._1sfeueqe')[1].text.replace('价格\n', '')
        type = rent.find_element_by_css_selector('div._wuffzwa').find_element_by_tag_name('small').text.split('·')
        # 房子类型
        house_type = type[0].strip()
        # 房间类型
        room_type = type[1].strip()

        # print(house_type, room_type)
        rent_room_list = [name, price, house_type, room_type]
        print(','.join(rent_room_list))


if __name__ == '__main__':
    main()
