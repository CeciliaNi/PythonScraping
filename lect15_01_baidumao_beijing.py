"""
作者：倪媛
功能：运用百度地图的API服务获取北京的公园信息
日期：19/11/2018
"""
import requests
import json


def main():
    """
    主函数
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36'}

    param = {
        'query': '公园',
        'region': '北京',
        'scope': '2',
        'page_size': '20',
        # 显示POI的第20页的结果数据
        'page_num': 20,
        'output': 'json',
        'ak': 'oQfNUXGikmA6RSmj5utnxgqCOkavWFjM'
    }
    url = 'http://api.map.baidu.com/place/v2/search'
    r = requests.get(url, params=param, headers=headers)

    decodejson = json.loads(r.text)

    print(decodejson)


if __name__ == '__main__':
    main()
