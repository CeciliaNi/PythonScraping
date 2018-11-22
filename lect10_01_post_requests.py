"""
作者：倪媛
功能：处理登录表单
日期：08/11/2018
"""
import requests
import http.cookiejar as cookielib

# 创建一个session对象
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')

try:
    session.cookies.load(ignore_discard=True)
except:
    print('Cookies未能加载')


def islogin():
    """
    检测是否已经登录
    """
    login_url = 'http://www.santostang.com/wp-admin/profile.php'
    login_code = session.get(login_url, allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False


def login(account, pwd):
    """
    登录函数
    """

    post_url = 'http://www.santostang.com/wp-login.php'

    # 构建POST请求的参数字典
    postdata = {
        'log': account,
        'pwd': pwd,
        'rememberme': 'forever',
        'redirect_to': 'http://www.santostang.com/wp-admin/',
        'testcookie': '1'
    }
    try:
        login_page = session.post(post_url, data=postdata)
        login_code = login_page.text
        print(login_page.status_code)
        print(login_code)
    except:
        pass

    session.cookies.save()


def main():
    """
    主函数
    """

    if islogin():
        print('您已经登录')
    else:
        login('test', 'a12345')


if __name__ == '__main__':
    main()
