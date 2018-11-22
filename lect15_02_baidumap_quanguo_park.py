"""
作者：倪媛
功能：利用百度地图提供的API服务统计全国所有地市的公园数
日期：20/11/2018
"""
import requests
import json
import time
import random


def get_jsondata(region, page_num=0):
    """
    获取每个省份地市的公园信息函数
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36'}

    param = {
        'query': '公园',
        'region': region,
        'output': 'json',
        'scope': '2',
        'page_size ': '20',
        'page_num': page_num,
        'ak': 'oQfNUXGikmA6RSmj5utnxgqCOkavWFjM'
    }
    url = 'http://api.map.baidu.com/place/v2/search'

    time.sleep(random.randint(2, 3))

    r = requests.get(url, params=param, headers=headers)
    decodedata = json.loads(r.text)

    return decodedata


def main():
    """
    主函数
    """
    # 这里写省份列表不写'全国'是因为，page_num=0只能取到第一页的数据，写全国的话就不能取完整，省份列表的话第一页20条基本上就可以取到
    province_list = ['江苏省', '浙江省', '广东省', '福建省', '山东省', '河南省',
                     '河北省', '四川省', '辽宁省', '云南省', '湖南省', '湖北省',
                     '江西省', '安徽省', '山西省', '广西壮族自治区', '陕西省', '黑龙江省',
                     '内蒙古自治区', '贵州省', '吉林省', '甘肃省', '新疆维吾尔自治区', '海南省',
                     '宁夏回族自治区', '青海省', '西藏自治区']

    # province_list = ['广西壮族自治区']

    for enchprovince in province_list:
        print(enchprovince)
        # 循环将每个省份信息带入函数获取每个省份的各个地市的公园信息
        decodejson = get_jsondata(enchprovince)

        for enchcity in decodejson['results']:
            cityname = enchcity['name']
            park_num = enchcity['num']
            # 输出城市拥有的公园数目信息
            out_put = cityname + '\t' + str(park_num) + '\n'

            with open('cities_park_num.txt', mode='a+', encoding='utf-8') as f:
                f.write(out_put)
                f.close()


if __name__ == '__main__':
    main()
