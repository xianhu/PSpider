# _*_ coding: utf-8 _*_

"""
yundama.py by xianhu
"""

import json
import time
import logging
import urllib.request
import spider


class YunDaMa(object):
    """
    class of YunDaMa, to identify captcha by yundama.com
    """

    def __init__(self, user_name, pass_word, appid=None, appkey=None, boundary=None):
        """
        constructor
        """
        self.base_url = "http://api.yundama.com/api.php"
        self.base_headers = spider.make_headers(
            user_agent="pc",
            host="api.yundama.com",
            referer="http://www.yundama.com/download/YDMHttp.html",
            accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            accept_language="zh-CN,zh;q=0.8",
            origin="http://www.yundama.com"
        )

        self.user_name = user_name
        self.pass_word = pass_word

        self.appid = "1" if not appid else appid
        self.appkey = "22cc5376925e9387a23cf797cb9ba745" if not appkey else appkey
        self.boundary = "----WebKitFormBoundaryIHXcDqOlNKqucLJ7" if not boundary else boundary
        return

    def get_captcha(self, file_bytes, file_name, file_type, codetype="1000", repeat=10):
        """
        get captcha result(cid, code), based on file_bytes, file_name, file_type(image/jpeg)
        :key: http://www.yundama.com/apidoc/YDM_ErrorCode.html
        :param codetype: http://www.yundama.com/price.html
        """
        cid = self.upload(file_bytes, file_name, file_type, codetype)
        if not cid:
            return None, None
        while repeat > 0:
            code = self.result(cid)
            if code:
                return cid, code
            repeat -= 1
            time.sleep(2)
        return cid, None

    def upload(self, file_bytes, file_name, file_type, codetype):
        """
        upload image file, return cid or None
        """
        post_data = spider.make_post_data({
            "username": self.user_name,
            "password": self.pass_word,
            "codetype": codetype,
            "appid": self.appid,
            "appkey": self.appkey,
            "timeout": 60,
            "method": "upload",
            "_file_image": [file_bytes, file_name, "file", file_type],
        }, boundary=self.boundary)
        try:
            request = urllib.request.Request(self.base_url, data=post_data, headers=self.base_headers)
            request.add_header("Content-Type", "multipart/form-data; boundary=%s" % self.boundary)
            json_data = json.loads(urllib.request.urlopen(request, timeout=60).read().decode("utf-8"))
        except Exception as excep:
            json_data = {"ret": -1, "errMsg": excep}
        logging.warning("YunDaMa upload %s: %s", "succeed" if json_data["ret"] == 0 else "failed", json_data)
        return json_data.get("cid", "")

    def result(self, cid):
        """
        get result from cid, return code or None
        """
        try:
            request = urllib.request.Request(self.base_url+("?cid=%d&method=result" % cid), headers=self.base_headers)
            json_data = json.loads(urllib.request.urlopen(request, timeout=10).read().decode("utf-8"))
        except Exception as excep:
            json_data = {"ret": -1, "errMsg": excep}
        logging.warning("YunDaMa result %s: %s", "succeed" if json_data["ret"] == 0 else "failed", json_data)
        return json_data.get("text", "")

    def report(self, cid):
        """
        report result of captcha, flag is 0
        """
        post_data = spider.make_post_data({
            "username": self.user_name,
            "password": self.pass_word,
            "appid": self.appid,
            "appkey": self.appkey,
            "cid": cid,
            "flag": 0,
            "method": "report",
        }, boundary=self.boundary)
        try:
            request = urllib.request.Request(self.base_url, data=post_data, headers=self.base_headers)
            request.add_header("Content-Type", "multipart/form-data; boundary=%s" % self.boundary)
            json_data = json.loads(urllib.request.urlopen(request, timeout=10).read().decode("utf-8"))
        except Exception as excep:
            json_data = {"ret": -1, "errMsg": excep}
        logging.warning("YunDaMa report %s: %s", "succeed" if json_data["ret"] == 0 else "failed", json_data)
        return

if __name__ == '__main__':
    ydm = YunDaMa("username", "password")
    cid_t, code_t = ydm.get_captcha(urllib.request.urlopen("http://www.yundama.com/index/captcha").read(),
                                    "captcha.jpeg", "image/jpeg", codetype="1000", repeat=10)
    print(cid_t, code_t)
    if cid_t and (not code_t):
        ydm.result(cid_t)
