""""
    作者：倪媛
    功能：ajax网页数据采集--唐松微博的评论数据采集
    日期：23/10/218
"""
import requests
import json


def get_page_comment(url):
    r = requests.get(url, timeout=30)
    # print(r.text)
    # 从 json数据中提取评论。上述的结果比较杂乱，但是它其实是 json 数据，我们可以使用 json 库解析数据，从中提取我们想要的数据。
    json_str = r.text
    # 仅仅提取字符串中符合json格式的部分
    json_str = json_str[json_str.find('{'):-2]
    # 使用 json.loads把json格式字符串转换为Python数据类型,这里已经转换成了字典类型
    json_data = json.loads(json_str)
    # 注意字典中嵌套了字典，所以先打开result,然后再打开字典parents,parents中是一个列表，列表中元素是字典[{},{},.....]
    comment_list = json_data['results']['parents']

    # 列表中的每个元素就是评论列表
    for comment in comment_list:
        content = comment['content']
        print(content)


def main():
    """
    主函数
    """
    # 拼接url,这个博客只有5页，offset从1到5循环
    for i in range(1, 6):
        # Python 用反斜线 (“\”) 作为续行符（换行符)
        url = 'https://api-zero.livere.com/v1/comments/list?callback=jQuery11240631120588642768_1540273552256&limit=10&offset='\
             + str(i)\
             + '&repSeq=4272904&requestPath=%2Fv1%2Fcomments%2Flist&consumerSeq=1020&livereSeq=28583&smartloginSeq=5154&_=1540273552261'

        get_page_comment(url)


if __name__ == '__main__':
    main()

