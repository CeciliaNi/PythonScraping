"""
作者：倪媛
功能：获取百度地图的公园信息 存入MySQL数据库
日期：20/11/2018
"""
import requests
import MySQLdb
import time
import json
import random

# # 建立MySQL连接，连接的数据库为scraping,这是前期的准备，所以将其注释掉
# conn = MySQLdb.connect(host='localhost', user='root',
#                        password='3edc#EDC', db='scraping', charset='utf8')
# cur = conn.cursor()
# # 建表,注意这里用的是三引号，
# sql = '''create table city(
#         id int not null auto_increment,
#         city varchar(200) not null,
#         park varchar(200) not null,
#         location_lat float,
#         location_lng float,
#         address varchar(200),
#         street_id varchar(200),
#         uid varchar(200),
#         create_time timestamp default current_timestamp,
#         primary key(id)
# );'''
#
# cur.execute(sql)
# cur.close()
# conn.commit()
# conn.close()

conn = MySQLdb.connect(host='localhost', user='root',
                       password='3edc#EDC', db='scraping', charset='utf8')
cur = conn.cursor()

city_list = []

with open('cities_park_num.txt', 'r', encoding='utf-8') as f:
    for enchline in f:
        if enchline != '':
            files = enchline.split('\t')
            city = files[0]
            city_list.append(city)
    f.close()

    print(len(city_list))


def get_json(region, pagenum):
    """
    获取制定页面的公园查询数据
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36'
    }
    param = {
        'query': '公园',
        'region': region,
        'page_size': 20,
        'scope': '2',
        'pagenum': pagenum,
        'output': 'json',
        'ak': 'oQfNUXGikmA6RSmj5utnxgqCOkavWFjM'
    }
    url = 'http://api.map.baidu.com/place/v2/search'
    # 这里要设置休眠时间，要不然并发量太大会限制访问
    time.sleep(random.randint(2, 3) + random.random())
    r = requests.get(url, params=param, headers=headers)

    decodedata = json.loads(r.text)
    return decodedata


def main():
    """
    主函数
    """
    for enchcity in city_list:
        pagenum = 0
        not_last_page = True
        while not_last_page:
            decodedata = get_json(enchcity, pagenum)
            # 获取results部分的数据 并循环获取每个公园的数据
            if decodedata['results']:
                for enchpark in decodedata['results']:
                    try:
                        park = enchpark['name']
                    except:
                        park = None

                    try:
                        location_lat = enchpark['location']['lat']
                    except:
                        location_lat = None

                    try:
                        location_lng = enchpark['location']['lng']
                    except:
                        location_lng = None

                    try:
                        address = enchpark['address']
                    except:
                        address = None

                    try:
                        street_id = enchpark['street_id']
                    except:
                        street_id = None

                    try:
                        uid = enchpark['uid']
                    except:
                        uid = None

                    sql = """insert into scraping.city(city,park,location_lat,location_lng,
                                address,street_id,uid) values ('{}','{}','{}','{}','{}','{}','{}')
                                """.format(enchcity, park, location_lat, location_lng, address, street_id, uid)
                    cur.execute(sql)
                    # 要记得提交
                    conn.commit()

                # 当读取完一页数据后 pagenum加1
                pagenum += 1

            else:
                # 当decodedata['results']为空时走else判断，这里把最后一页标志设为False结束循环
                not_last_page = False

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
