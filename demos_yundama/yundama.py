# _*_ coding: utf-8 _*_

"""
yundama.py by xianhu
"""

import time
import spider
import logging
import requests


class YunDaMa(object):
    """
    class of YunDaMa, to identify captcha by yundama.com
    """

    def __init__(self, user_name, pass_word, appid=None, appkey=None):
        """
        constructor
        """
        self.base_url = "http://api.yundama.com/api.php"
        self.base_headers = {
            "User-Agent": spider.make_random_useragent("pc"),
            "Host": "api.yundama.com",
            "Referer": "http://www.yundama.com/download/YDMHttp.html",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Origin": "http://www.yundama.com",
        }

        self.user_name = user_name
        self.pass_word = pass_word

        self.appid = "1" if not appid else appid
        self.appkey = "22cc5376925e9387a23cf797cb9ba745" if not appkey else appkey
        return

    def get_captcha(self, file_name, file_bytes, file_type="image/jpeg", codetype="1000", repeat=10):
        """
        get captcha result(cid, code), based on file_name, file_bytes, file_type
        :key: http://www.yundama.com/apidoc/YDM_ErrorCode.html
        :param codetype: http://www.yundama.com/price.html
        """
        cid = self.upload(file_name, file_bytes, file_type, codetype)
        if not cid:
            return None, None
        while repeat > 0:
            code = self.result(cid)
            if code:
                return cid, code
            repeat -= 1
            time.sleep(2)
        return cid, None

    def upload(self, file_name, file_bytes, file_type, codetype):
        """
        upload image file, return cid or None
        """
        post_data = {
            "username": self.user_name,
            "password": self.pass_word,
            "codetype": codetype,
            "appid": self.appid,
            "appkey": self.appkey,
            "timeout": 60,
            "method": "upload",
        }
        files = {"file": (file_name, file_bytes, file_type)}
        try:
            response = requests.post(self.base_url, data=post_data, headers=self.base_headers, files=files)
            json_data = response.json()
        except Exception as excep:
            json_data = {"ret": -1, "errMsg": excep}
        logging.warning("YunDaMa upload %s: %s", "succeed" if json_data["ret"] == 0 else "failed", json_data)
        return json_data.get("cid", "")

    def result(self, cid):
        """
        get result from cid, return code or None
        """
        try:
            response = requests.get(self.base_url+("?cid=%d&method=result" % cid), headers=self.base_headers)
            json_data = response.json()
        except Exception as excep:
            json_data = {"ret": -1, "errMsg": excep}
        logging.warning("YunDaMa result %s: %s", "succeed" if json_data["ret"] == 0 else "failed", json_data)
        return json_data.get("text", "")


if __name__ == '__main__':
    ydm = YunDaMa("username", "password")
    cid_t, code_t = ydm.get_captcha("captcha.jpeg", requests.get("http://www.yundama.com/index/captcha").content)
    print(cid_t, code_t)
    if cid_t and (not code_t):
        ydm.result(cid_t)
