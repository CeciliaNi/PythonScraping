"""
作者：倪媛
功能：单线程爬取1000个网页
日期：05/11/2018
"""
import time
import requests


def main():
    """
    主函数
    """
    # 打开网页列表
    with open('alexa.txt', mode='r') as f:
        # 获取网页列表
        website_list = f.readlines()
        # 循环读取网页列表
        web_link_list = []
        for website in website_list:
            web_link = website.split('\t')[1]
            web_link = web_link.replace('\n', '')
            web_link_list.append(web_link)

    start_time = time.time()
    print(start_time)

    for enchone in web_link_list:
        try:
            r = requests.get(enchone, timeout=20)
            print(r.status_code, enchone)
        except Exception as e:
            print('Error', e)

    end_time = time.time()
    print(end_time)

    print('串行的总时间为：', end_time - start_time)


if __name__ == '__main__':
    main()
