"""
作者：倪媛
功能：进行深圳前海蛇口片区的经纬度进行提取
日期：14/11/2018
"""
from selenium import webdriver
import time
import csv
import random

x_n = 22.56
x_s = 22.45
y_w = 113.88
y_e = 113.96


def get_info_list(driver, search_type):
    """
    获取右侧展示信息列表
    """
    project_list = []
    li_list = driver.find_element_by_css_selector('ul.local_s').find_elements_by_tag_name('li')
    # 循环展示列表 获取具体信息
    for li in li_list:
        obj_type = search_type
        name = li.find_element_by_tag_name('a').text.strip()
        a_p_list = li.find_element_by_tag_name('p').text.split('\n')
        position = a_p_list[len(a_p_list)-1].strip()
        # 判断是否在蛇口前海片区，如果在将具体信息写入列表
        jingdu = eval(position.split(',')[0].replace('坐标：', ''))
        weidu = eval(position.split(',')[1])

        if (jingdu >= y_w) and (jingdu <= y_e) and (weidu >= x_s) and (weidu <= x_n):
            info_list = [obj_type, name, jingdu, weidu]
            project_list.append(info_list)

    return project_list


def main():

    """
    主函数
    :return:
    """
    url = 'http://api.map.baidu.com/lbsapi/getpoint/index.html?qq-pf-to=pcqq.c2c'
    driver = webdriver.Chrome()
    # 窗口最大化
    driver.maximize_window()
    # 设置等待超时时间
    driver.implicitly_wait(30)
    driver.get(url)

    # 将位置定位在深圳 并在点击查询后清空搜索框
    driver.find_element_by_css_selector('input.text').send_keys('深圳')
    driver.find_element_by_css_selector('input.button').click()
    driver.find_element_by_css_selector('input.text').clear()

    # 将获取到的数据写入csv文件
    filepath = '剩余几种类型.csv'
    with open(filepath, mode='w', encoding='utf-8', newline='') as f:
        # 写入头信息,csv的reader出来的行是列表和write的的参数也是列表
        header = ['类型', '名称', '经度', '纬度']
        writer = csv.writer(f)
        writer.writerow(header)

        # 查询列表
        search_list = ['药店', '咖啡厅', '图书馆', '加油站', '电影院',
                       '体育馆', '银行', '菜市场', '营业厅']

        # search_list = ['老广']

        for enchone in search_list:
            search_type = enchone
            driver.find_element_by_css_selector('input.text').send_keys(search_type)
            driver.find_element_by_css_selector('input.button').click()

            sleep_time3 = 3 + random.random()
            time.sleep(sleep_time3)

            result_list = get_info_list(driver, search_type)
            # 将第一页写入csv文件
            for project in result_list:
                writer.writerow(project)
            # 后面一次点击下一页获取数据并写入CSV

            next_page_num = len(driver.find_elements_by_xpath("//a[text()='下一页']"))
            while next_page_num == 1:

                driver.find_element_by_xpath("//a[text()='下一页']").click()
                sleep_time2 = 3 + random.random()
                time.sleep(sleep_time2)

                # 查看此页列表的个数 是否为0 如果不为0 跳出循环
                try:
                    list_num = driver.find_element_by_css_selector('ul.local_s').find_elements_by_tag_name('li')
                    if len(list_num) == 0:
                        break
                except Exception as e:
                    break

                result_list = get_info_list(driver, search_type)
                # 写入csv文件
                for project in result_list:
                    writer.writerow(project)

                # 判断是否有下一页
                next_page_num = len(driver.find_elements_by_xpath("//a[text()='下一页']"))

            driver.find_element_by_css_selector('input.text').clear()

    time.sleep(3)


if __name__ == '__main__':
    main()
