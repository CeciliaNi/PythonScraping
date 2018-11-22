"""
作者：倪媛
功能：维基百科链接广度爬虫
日期：16/11/2018
"""
import requests
import re
import threading
import time

# 互斥锁
g_mutex = threading.Condition()
# 获取的每个深度的页面html
g_pages = []
# 等待爬取的url链接列表
g_queueurl = []
# 已经爬取过的url链接列表
g_existurl = []
# 找到的链接数
g_writecount = 0

time1 = time.time()


class Clawler:
    """
    爬取工具类
    """
    def __init__(self, url, threadnum):
        self.url = url
        self.threadnum = threadnum
        self.threadpool = []

    def craw(self):
        global g_queueurl
        global g_pages
        g_queueurl.append(self.url)
        depth = 1

        while depth < 3:
            print('Searching depth ', depth, '...\n')
            self.downloadall()
            self.update()
            g_pages = []
            depth += 1

    def downloadall(self):
        global g_queueurl
        i = 0
        while i < len(g_queueurl):
            j = 0
            while j < self.threadnum and i+j < len(g_queueurl):
                self.download(g_queueurl[i+j], j)
                j += 1
            i += j

            for thread in self.threadpool:
                thread.join(30)

            self.threadpool = []

        g_queueurl = []

    def download(self, url, tid):
        crawthread = ClawlerThread(url, tid)
        self.threadpool.append(crawthread)
        crawthread.start()

    def update(self):
        global g_queueurl
        global g_existurl
        newurllist = []

        for page in g_pages:
            newurllist += self.geturl(page)
        g_queueurl = list(set(newurllist) - set(g_existurl))

    def geturl(self, page):
        link_list = re.findall('<a href="/wiki/([^:#=<>]*?)".*?</a>', page)
        unique_list = list(set(link_list))
        return unique_list


class ClawlerThread(threading.Thread):
    """
    爬虫线程工具类
    """
    def __init__(self, url, tid):
        threading.Thread.__init__(self)
        self.url = url
        self.tid = tid

    def run(self):
        """
        具体爬虫过程
        """
        # 使用全局变量
        global g_mutex
        global g_writecount

        try:
            print(self.tid, 'crawl', self.url)
            r = requests.get('https://en.wikipedia.org/wiki/'+self.url)
            html = r.text
            # 找出当前爬取页面的所有词条 并去重
            link_list = re.findall('<a href="/wiki/([^:#=<>]*?)".*?</a>', html)
            unique_list = list(set(link_list))

            # 循环词条
            for unique in unique_list:
                g_writecount += 1
                output = 'No.'+str(g_writecount)+'\tThread'+str(self.tid)+'\t'+self.url+'->'+unique
                print(output)

                with open('wiki_url_width.txt', mode='a+', encoding='utf-8')as f:
                    f.write(output)
                    f.close()
        except Exception as e:
            g_mutex.acquire()
            g_existurl.append(self.url)
            g_mutex.release()
            print('Failed downloading and saving', self.url)
            print(e)
            return None
        g_mutex.acquire()
        g_pages.append(html)
        g_existurl.append(self.url)
        g_mutex.release()


def main():
    """
    主函数
    """
    url = 'Wikipedia'
    # 限定线程数目为5个
    thread_num = 5
    crawler = Clawler(url, thread_num)
    crawler.craw()

    print('total time is ', time.time() - time1)


if __name__ == '__main__':
    main()
