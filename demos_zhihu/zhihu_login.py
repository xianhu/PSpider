# _*_ coding: utf-8 _*_

"""
define login_zhihu to login zhihu.com, just as a demonstration
"""

import re
import time
import json
import logging
import urllib.parse
import urllib.request
import http.cookiejar


def login_zhihu(user_name, pass_word):
    """
    login zhihu.com, just as a demonstration
    """
    cookie_handler = urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
    urllib.request.install_opener(urllib.request.build_opener(cookie_handler))

    # get _xsrf
    response = urllib.request.urlopen("http://www.zhihu.com")
    data = response.read().decode("utf-8")
    _xsrf = re.search("name=\"_xsrf\" value=\"(?P<value>.*)\"", data).group("value")

    # get captcha
    response = urllib.request.urlopen('http://www.zhihu.com/captcha.gif?r=%d&type=login' % int(time.time() * 1000))
    with open('captcha.jpg', 'wb') as file_image:
        file_image.write(response.read())
    captcha = input("input the captcha: ")

    # login
    url = "http://www.zhihu.com/login/email"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:41.0) Gecko/20100101 Firefox/41.0",
        "Referer": "http://www.zhihu.com/"
    }
    post_data = urllib.parse.urlencode({
        "_xsrf": _xsrf,
        "email": user_name,
        "password": pass_word,
        "captcha": captcha,
        "remember_me": "true"
    }).encode()
    response = urllib.request.urlopen(urllib.request.Request(url, data=post_data, headers=headers))
    result = json.loads(response.read().decode("utf-8"))

    if result["r"] == 0:
        logging.warning("login zhihu success!")
        return True
    logging.error("login zhihu failed! %s" % str(result))
    return False
