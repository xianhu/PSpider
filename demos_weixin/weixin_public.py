# _*_ coding: utf-8 _*_

import sys
import time
import json
import spider
import logging
import urllib.parse
import urllib.request
from queue import Queue
from bs4 import BeautifulSoup


class WeiXinPublic(object):
    """
    class of WeiXinPublic
    """

    def __init__(self, max_repeat=5):
        """
        constructor
        """
        self.base_url = "http://weixin.sogou.com/"
        self.base_url_gzhjs = "http://weixin.sogou.com/gzhjs?"
        self.base_url_weixin = "http://weixin.sogou.com/weixin?"
        self.base_url_antispider = "http://weixin.sogou.com/antispider/"
        self.base_url_weixinqq = "http://mp.weixin.qq.com/"

        self.fetch_queue = Queue()      # unfetched url queue (url, keys, repeat)
        self.saved_set = set()          # saved url or other id
        self.current_page = 1           # current page which is fetching
        self.max_repeat = max_repeat    # maxinum repeat time

        self.arts_key = None            # key words for fetching articals
        self.user_id = None             # user id, not the open_id; None if fetch_type is 2
        self.search_keys = None         # search keys, (key, others)

        self.fetch_type = 1             # fetch type, 1: public_user, 2: public_artical
        self.fetch_tsn = 0              # fetch tsn, 0: all, 1: one day, 2: one week, 3: one month

        self.cookie_jar, self.opener = spider.make_cookiejar_opener()
        self.opener.addheaders = spider.make_headers(
            user_agent="pc",
            host="weixin.sogou.com",
            accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            accept_encoding="gzip, deflate",
            accept_language="zh-CN"
        ).items()

        # prepare to identify the captcha, and reset this class
        self.yundama = spider.YunDaMa("qixianhu", "mimaMIMA123456")
        self.file_out = None
        return

    def fetch_user(self, user_id, file_out=sys.stdout):
        """
        fetch user
        """
        self.file_out = file_out
        self.user_id = user_id
        self.search_keys = ("user_search", user_id)

        self.fetch_type = 1
        self.fetch_tsn = 0

        self.reset_this_class()
        self.work()
        return

    def fetch_arts(self, arts_key, fetch_tsn=0, file_out=sys.stdout):
        """
        fetch articles
        """
        self.file_out = file_out
        self.arts_key = arts_key
        self.search_keys = ("arts_search", arts_key)

        self.fetch_type = 2
        self.fetch_tsn = fetch_tsn

        self.reset_this_class()
        self.work()
        return

    def reset_this_class(self):
        """
        reset this class
        """
        post_dict = {
            "type": self.fetch_type,
            "query": self.arts_key if self.fetch_type == 2 else self.user_id,
            "ie": "utf-8",
            "_sug_": "n",
            "_sug_type_": "",
            "t": int(time.time() * 1000)
        }
        if self.fetch_type == 2:
            post_dict["tsn"] = self.fetch_tsn
            post_dict["page"] = self.current_page
        post_data = urllib.parse.urlencode(post_dict)

        self.fetch_queue.queue.clear()
        self.fetch_queue.put(item=(self.base_url_weixin+post_data, self.search_keys, 0))
        logging.debug("WeiXinPublic reset_this_class success: current_page=%d" % self.current_page)
        return

    def work(self):
        """
        process of fetching and parsing
        """
        while self.fetch_queue.qsize() > 0:
            url, keys, repeat = self.fetch_queue.get()
            logging.debug("WeiXinPublic work: keys=%s, repeat=%d, url=%s" % (str(keys), repeat, url))
            try:
                response = self.opener.open(url, timeout=5)
                if keys[0] == "user_search":
                    self.parse_user_search(url, keys, response)

                if keys[0] == "user_arts":
                    self.parse_user_arts(url, keys, response)

                if keys[0] == "arts_search":
                    self.parse_arts_search(url, keys, response)

                if keys[0] == "get_art":
                    self.parse_get_art(url, keys, response)
            except Exception as excep:
                if repeat < self.max_repeat:
                    self.fetch_queue.put(item=(url, keys, repeat+1))
                else:
                    logging.error("WeiXinPublic work: error=%s, url=%s" % (str(excep), url))
        return

    def parse_user_search(self, url, keys, response):
        """
        parser, keys: ("user_search", user_id)
        """
        soup = BeautifulSoup(spider.get_html_content(response, charset="utf-8"), "html.parser")
        if not self.check_anti_by_captcha(soup):
            self.reset_this_class()
            return

        user_name = ""
        for user_item in soup.find_all("div", class_="wx-rb bg-blue wx-rb_v1 _item"):
            if user_item.find("label", attrs={"name": "em_weixinhao"}).get_text() == self.user_id:
                user_name = user_item.find("div", class_="txt-box").find("h3").get_text()
                self.fetch_queue.put(item=(user_item.get("href"), ("user_arts", self.user_id, user_name), 0))
        logging.debug("WeiXinPublic parse_user_search: user_name=%s" % user_name)
        return

    def parse_user_arts(self, url, keys, response):
        """
        parser, keys: ("user_arts", user_id, user_name)
        """
        html = spider.get_html_content(response, charset="utf-8")
        json_data = spider.get_json_data(html, "msgList = '(?P<item>\{[\w\W]+?\})'")
        if json_data:
            for item in json_data.get("list", []):
                item_url = spider.get_url_legal(item["app_msg_ext_info"]["content_url"][1:], self.base_url_weixinqq).replace("&amp;", "&")
                self.fetch_queue.put(item=(item_url, ("get_art", None, keys[1], keys[2]), 0))
                for subitem in item["app_msg_ext_info"]["multi_app_msg_item_list"]:
                    subitem_url = spider.get_url_legal(subitem["content_url"][1:], self.base_url_weixinqq).replace("&amp;", "&")
                    self.fetch_queue.put(item=(subitem_url, ("get_art", None, keys[1], keys[2]), 0))
        logging.debug("WeiXinPublic parse_user_arts: len(fetch_queue)=%d" % self.fetch_queue.qsize())
        return

    def parse_arts_search(self, url, keys, response):
        """
        parser, keys: ("arts_search", arts_key)
        """
        _, querys = spider.get_url_params(url)
        self.current_page = int(querys["page"][0]) if "page" in querys else self.current_page
        logging.debug("WeiXinPublic parse_arts_search: update current page, current_page=%d" % self.current_page)

        soup = BeautifulSoup(spider.get_html_content(response, charset="utf-8"), "html.parser")
        if not self.check_anti_by_captcha(soup):
            self.reset_this_class()
            return

        # current page
        for art_soup in soup.find_all("div", class_="txt-box"):
            art_url = spider.get_url_legal(art_soup.find("a").get("href"), base_url=url)
            user_openid = art_soup.find("a", id="weixin_account").get("i")
            user_name = art_soup.find("a", id="weixin_account").get("title")
            self.fetch_queue.put(item=(art_url, ("get_art", keys[1], user_openid, user_name), 0))

        # next page
        next_page = soup.find("a", id="sogou_next")
        if next_page:
            next_page_url = spider.get_url_legal(next_page.get("href"), base_url=url)
            self.fetch_queue.put(item=(next_page_url, keys, 0))
        return

    def parse_get_art(self, url, keys, response):
        """
        parser, keys: ("get_art", None or arts_key, user_id or user_openid, user_name)
        """
        soup = BeautifulSoup(spider.get_html_content(response, charset="utf-8"), "html.parser")

        _, querys = spider.get_url_params(url)
        s_title = spider.get_string_strip(soup.title.string)
        s_date = soup.find("em", id="post-date").get_text()
        self.file_out.write("\t".join([s_title, s_date, str(keys[1:])]) + "\n")

        self.saved_set.add(keys[2] + s_date + s_title)
        logging.debug("WeiXinPublic parse_get_art: len(saved_set)=%d" % len(self.saved_set))
        return

    def check_anti_by_captcha(self, soup):
        """
        check anti-spider by captcha
        :return 1, 0: 1(can continue), 0(can repeat)
        """
        if not soup.find("img", id="seccodeImage"):
            return 1

        while 1:
            cid, code = None, None
            while not code:
                captcha_url = soup.find("img", id="seccodeImage").get("src")
                response = self.opener.open(spider.get_url_legal(captcha_url, self.base_url_antispider))
                cid, code = self.yundama.get_captcha(response.read(), "captcha.jpeg", "image/jpeg", codetype="1006")

            post_data = urllib.parse.urlencode({
                "c": code,
                "r": soup.find("input", id="from").get("value"),
                "v": 5
            }).encode()
            response = self.opener.open("http://weixin.sogou.com/antispider/thank.php", data=post_data)

            json_data = json.loads(spider.get_html_content(response, charset="utf-8"))
            if json_data["msg"].find("解封成功") >= 0:
                snuid = json_data["id"]
                self.cookie_jar.set_cookie(spider.make_cookie(name="SNUID", value=snuid, domain="weixin.sogou.com"))

                post_dict = {
                    "uigs_productid": "webapp",
                    "type": "antispider",
                    "subtype": "",
                    "domain": "weixin",
                    "suv": "",
                    "snuid": snuid,
                    "t": int(time.time() * 1000)
                }
                for cookie in self.cookie_jar:
                    if cookie.name == "SUV":
                        post_dict["suv"] = cookie.value

                post_dict["subtype"] = "0_seccodeInputSuccess"
                post_dict["t"] = int(time.time() * 1000)
                self.opener.open("http://pb.sogou.com/pv.gif?" + urllib.parse.urlencode(post_dict))

                post_dict["subtype"] = "close_refresh"
                post_dict["t"] = int(time.time() * 1000)
                self.opener.open("http://pb.sogou.com/pv.gif?" + urllib.parse.urlencode(post_dict))
                break
            else:
                self.yundama.report(cid=cid) if cid else 0
        logging.warning("WeiXinPublic check_anti_by_captcha: anti-spider success!")
        return 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")

    weixin = WeiXinPublic()
    # weixin.fetch_user(user_id="diyCRT")
    # weixin.fetch_arts("北京国安", fetch_tsn=0)
    exit()
