"""
作者：倪媛
功能：通过大众点评的搜索结果获取餐厅的基本信息和地址
日期：21/11/2018
"""
from selenium import webdriver
import time
import csv


# 打开chrome浏览器
driver = webdriver.Chrome()
# 窗口最大化
driver.maximize_window()
# 设置隐性等待20s
driver.implicitly_wait(20)


def get_page_food():
    """
    获取每页的商家美食信息
    """
    result_list = []
    # 获取点评中的列表元素 注意这里的tr元素要从第二个开始取，因为第一个是表头
    ten_food_list = driver.find_elements_by_xpath('//table/tbody/tr[position()>1]')
    for food in ten_food_list:
        # 商家名称
        shop = food.find_element_by_css_selector('td.td-shopName')
        shopname = shop.text.strip()
        # 商家链接
        shoplink = shop.find_element_by_tag_name('a').get_attribute('href')
        # 商区
        region_name = food.find_element_by_css_selector('td.td-mainRegionName').text.strip()
        # 口味评分
        refinedScore1 = food.find_element_by_css_selector('td.td-refinedScore1').text.strip()
        # 坏境评分
        refinedScore2 = food.find_element_by_css_selector('td.td-refinedScore2').text.strip()
        # 服务评分
        refinedScore3 = food.find_element_by_css_selector('td.td-refinedScore3').text.strip()
        # 人均消费
        avgprice = food.find_element_by_css_selector('td.td-avgPrice').text.strip()

        food_list = [shopname, shoplink, region_name, refinedScore1, refinedScore2, refinedScore3, avgprice]
        result_list.append(food_list)

    return result_list


def main():
    """
    主函数
    """

    # 打开网页
    url = 'http://www.dianping.com/shoplist/shopRank/pcChannelRankingV2?rankId=707a1030132ea9515106357bb5758e47'
    driver.get(url)
    time.sleep(10)

    # 将爬取结果写入csv文件
    with open('dianping.csv', mode='w', encoding='utf-8', newline='') as f:
        header = ['商家名称', '商家链接', '商区', '口味评分', '环境评分', '服务评分', '人均消费']
        writer = csv.writer(f)
        writer.writerow(header)
        # 先将第一页写入文件 后面再通过有无下一页判断来获取
        food_info_list = get_page_food()
        # 将返回的美食列表信息逐行写入csv文件中
        for food_info in food_info_list:
            writer.writerow(food_info)

        # 判断是否有下一页元素
        next_page_num = len(driver.find_elements_by_css_selector('a.next'))

        while next_page_num == 1:
            # 点击下一页
            driver.find_element_by_xpath("//a[text()='下一页']").click()
            food_info_list = get_page_food()
            # 将返回的美食列表信息逐行写入csv文件中
            for food_info in food_info_list:
                writer.writerow(food_info)

            # 重新将下一页元素个数赋值
            next_page_num = len(driver.find_elements_by_css_selector('a.next'))


if __name__ == '__main__':
    main()
