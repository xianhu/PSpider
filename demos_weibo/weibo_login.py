# _*_ coding: utf-8 _*_

import re
import rsa
import ssl
import time
import json
import queue
import base64
import spider
import logging
import binascii
import urllib.parse
ssl._create_default_https_context = ssl._create_unverified_context


class WeiBoLogin(object):
    """
    class of WeiBoLogin, to login weibo.com
    """

    def __init__(self):
        """
        constructor
        """
        self.user_name = None
        self.pass_word = None
        self.user_uniqueid = None
        self.user_nick = None

        self.cookie_jar, self.opener = None, None
        self.yundama = spider.YunDaMa("", "")
        return

    def login(self, user_name, pass_word, proxies=None):
        """
        login weibo.com, return True or False
        """
        self.user_name = user_name
        self.pass_word = pass_word
        self.user_uniqueid = None
        self.user_nick = None

        self.cookie_jar, self.opener = spider.make_cookiejar_opener(is_cookie=True, proxies=proxies)
        self.opener.addheaders = spider.make_headers(
            user_agent="pc",
            host="weibo.com",
            referer="http://weibo.com/",
            accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            accept_encoding="gzip, deflate",
            accept_language="zh-CN,zh;q=0.8"
        ).items()
        self.opener.open("http://weibo.com/login.php")

        # get json data
        s_user_name = self.get_username()
        json_data = self.get_json_data(su_value=s_user_name)
        if not json_data:
            return False
        s_pass_word = self.get_password(json_data["servertime"], json_data["nonce"], json_data["pubkey"])

        # make post_dict
        post_dict = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "userticket": "1",
            "vsnf": "1",
            "service": "miniblog",
            "encoding": "UTF-8",
            "pwencode": "rsa2",
            "sr": "1280*800",
            "prelt": "529",
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "rsakv": json_data["rsakv"],
            "servertime": json_data["servertime"],
            "nonce": json_data["nonce"],
            "su": s_user_name,
            "sp": s_pass_word,
            "returntype": "TEXT",
        }

        # get captcha code
        if json_data["showpin"] == 1:
            url = "http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s" % (int(time.time()), json_data["pcid"])
            cid, code = self.yundama.get_captcha(self.opener.open(url).read(), "captcha.jpeg", "image/jpeg", codetype="1005")
            if not code:
                return False
            else:
                post_dict["pcid"] = json_data["pcid"]
                post_dict["door"] = code

        # login weibo.com
        login_url_1 = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=%d" % int(time.time())
        json_data_1 = json.loads(spider.get_html_content(self.opener.open(login_url_1, data=spider.make_post_data(post_dict))))
        if json_data_1["retcode"] == "0":
            # callback
            post_dict = {
                "callback": "sinaSSOController.callbackLoginStatus",
                "ticket": json_data_1["ticket"],
                "ssosavestate": int(time.time()),
                "client": "ssologin.js(v1.4.18)",
                "_": int(time.time()*1000),
            }
            login_url_2 = "https://passport.weibo.com/wbsso/login?" + urllib.parse.urlencode(post_dict)
            html_data = spider.get_html_content(self.opener.open(login_url_2), charset="gbk")
            json_data_2 = json.loads(re.search("\((?P<result>.*)\)", html_data).group("result"))
            if json_data_2["result"] is True:
                self.user_uniqueid = json_data_2["userinfo"]["uniqueid"]
                self.user_nick = json_data_2["userinfo"]["displayname"]
                logging.warning("WeiBoLogin succeed: %s", json_data_2)
            else:
                logging.warning("WeiBoLogin failed: %s", json_data_2)
        else:
            logging.warning("WeiBoLogin failed: %s", json_data_1)
        return True if self.user_uniqueid and self.user_nick else False

    def get_username(self):
        """
        get legal username
        """
        username_quote = urllib.parse.quote_plus(self.user_name)
        username_base64 = base64.b64encode(username_quote.encode("utf-8"))
        return username_base64.decode("utf-8")

    def get_json_data(self, su_value):
        """
        get the value of "servertime", "nonce", "pubkey", "rsakv" and "showpin", etc
        """
        post_data = urllib.parse.urlencode({
            "entry": "weibo",
            "callback": "sinaSSOController.preloginCallBack",
            "rsakt": "mod",
            "checkpin": "1",
            "client": "ssologin.js(v1.4.18)",
            "su": su_value,
            "_": int(time.time()*1000),
        })

        try:
            response = self.opener.open('http://login.sina.com.cn/sso/prelogin.php?'+post_data)
            data = spider.get_html_content(response, charset="utf-8")
            json_data = json.loads(re.search("\((?P<data>.*)\)", data).group("data"))
        except Exception as excep:
            json_data = {}
            logging.error("WeiBoLogin get_json_data error: %s", excep)

        logging.debug("WeiBoLogin get_json_data: %s", json_data)
        return json_data

    def get_password(self, servertime, nonce, pubkey):
        """
        get legal password, encrypt file: http://i.sso.sina.com.cn/js/ssologin.js
        """
        string = (str(servertime) + '\t' + str(nonce) + '\n' + str(self.pass_word)).encode("utf-8")
        public_key = rsa.PublicKey(int(pubkey, 16), int("10001", 16))
        password = rsa.encrypt(string, public_key)
        password = binascii.b2a_hex(password)
        return password.decode()


class WeiBoBase(WeiBoLogin):
    """
    class of WeiBoBase, as a base class
    """
    def __init__(self, users_pair=None):
        """
        constructor, users_pair: [(u1, p1), (u2, p2), ...]
        """
        WeiBoLogin.__init__(self)

        self.users_pair = users_pair
        self.users_index = 0

        self.base_url = "http://weibo.com/"
        self.header_re = re.compile("\$CONFIG\[[\'\"](?P<key>[\w]+?)[\'\"]\]=[\'\"](?P<value>[\w]*?)[\'\"]")

        self.fetch_queue = queue.Queue()    # unfetched url queue (url, keys, repeat)
        self.saved_set = set()              # saved url or other id

        self.current_page = 1               # current page which is fetching
        self.max_repeat = 5                 # maxinum repeat time
        self.out_file = None                # output file
        self.out_list = []                  # output list
        self.out_length = 0                 # output length
        return

    def re_login(self):
        """
        login repeat according to self.users_index
        """
        user_name, pass_word = self.users_pair[self.users_index % len(self.users_pair)]
        if not self.login(user_name, pass_word):
            exit()
        self.users_index += 1
        return
