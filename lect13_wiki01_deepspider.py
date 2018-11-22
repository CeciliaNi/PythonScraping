"""
作者：倪媛
功能：维基百科链接深度爬虫
日期：13/11/2018
"""
import time
import requests
import re


time1 = time.time()
g_write_count = 0
exist_url = []


def scrapy(url, depth=1):
    """
    爬取过程函数
    """
    # 使变量g_write_count全局化 表示在这里使用的是全局变量，而不是局部变量
    global g_write_count

    try:
        r = requests.get('https://en.wikipedia.org/wiki/'+url)
        html = r.text
        # print(html)
    except Exception as e:
        # 如果网址无法访问 将加入到exist_url列表
        print('Failed downloading and saving', url)
        print(e)
        exist_url.append(url)
        return None

    exist_url.append(url)

    # 获取当前访问网页的所有有效链接,在网址以/wiki/开头，且链接中不包含#=<>
    link_list = re.findall('<a href="/wiki/([^:#=<>]*?)".*?</a>', html)
    # 去除exist_url部分，请注意这里先转换为集合后取不包含exist_url部分
    unique_list = list(set(link_list)-set(exist_url))

    for unique in unique_list:
        g_write_count += 1
        output = 'No.' + str(g_write_count) + '\t Depath:' + str(depth) + \
                 '\t' + url + '->' + unique
        print(output)

        with open('wiki_url.txt', mode='a', encoding='utf-8') as f:
            f.write(output)
            f.close()

        if depth < 2:
            scrapy(unique, depth+1)


def main():
    """
    主函数
    """
    url = 'Wikipedia'

    scrapy(url)

    time2 = time.time()

    print('total time is ', time2 - time1)


if __name__ == '__main__':
    main()
