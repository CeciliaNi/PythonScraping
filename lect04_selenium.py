"""
    作者：倪媛
    功能：selenium模拟浏览器抓取
    日期：23/10/2018
"""
from selenium import webdriver
import time


def main():
    """
    主函数
    """
    # # url = 'http://www.santostang.com/2018/07/04/hello-world/'
    # # driver = webdriver.Firefox()
    # # driver.get(url, timeout=30)
    # caps = webdriver.DesiredCapabilities().FIREFOX
    # caps['marionette'] = True
    #
    # binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
    # driver = webdriver.Firefox(firefox_binary=binary, capabilities=caps)
    # driver.get('http://www.santostang.com/2018/07/04/hello-world/')

    # 控制图片加载
    # chrome_options = webdriver.ChromeOptions()
    # prefs = {'profile.default_content_setting_values':
    #             {
    #                 'images': 2,
    #                 'javascript': 2
    #             }
    #         }
    # chrome_options.add_experimental_option('prefs', prefs)
    # driver = webdriver.Chrome(chrome_options=chrome_options)

    driver = webdriver.Chrome()
    # 窗口最大化
    driver.maximize_window()
    # 设置等待超时时间
    driver.implicitly_wait(30)
    url = 'http://www.santostang.com/2018/07/04/hello-world/'
    driver.get(url)
    # print(driver.page_source)
    driver.switch_to.frame(driver.find_element_by_css_selector('iframe[title=''livere'']'))
    # print(driver.page_source)

    # 查询出满足条件的第一个元素
    # comment = driver.find_element_by_css_selector('div.reply-content')
    # content = comment.find_element_by_tag_name('p')
    # print(content.text)

    # 循环点击查看更多
    for i in range(4):
        driver.find_element_by_css_selector('button.more-btn').click()
        # 等待3秒
        time.sleep(3)

    # 查询出满足条件的所有元素,这里的comments是一个list
    comments = driver.find_elements_by_class_name('reply-content')
    print(type(comments))
    for comment in comments:
        content = comment.find_element_by_tag_name('p')
        print(content.text)


if __name__ == '__main__':
    main()
