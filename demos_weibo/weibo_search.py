# _*_ coding: utf-8 _*_

import re
import bs4
import time
import json
import spider
import logging
import datetime
import urllib.parse
from .weibo_login import WeiBoBase


class WeiBoSearch(WeiBoBase):
    """
    class of WeiBoSearch
    """

    def __init__(self, users_pair):
        """
        constructor
        """
        WeiBoBase.__init__(self, users_pair=users_pair)

        # parameters which are needed in this class
        self.search_url = "http://s.weibo.com/weibo/"
        self.fetch_keys = tuple()       # type: (A, B, ...)
        self.fetch_timescope = None     # type: custom:2016-04-01-0:2016-04-02
        self.fetch_type = None          # type: typeall=1, xsort=hot, scope=ori
        return

    def update_fetch_queue(self):
        """
        update fetch queue
        """
        search_url = self.search_url + urllib.parse.quote(urllib.parse.quote(" ".join(self.fetch_keys)))
        search_url += "&%s&suball=1&timescope=%s&page=%d" % (self.fetch_type, self.fetch_timescope, self.current_page)
        self.fetch_queue.put(item=(search_url, "search", 0))
        return

    def fetch_search_weibo(self, fetch_keys, fetch_timescope, fetch_type="typeall=1", out_file=None):
        """
        fetch search weibo
        """
        assert fetch_type in ["typeall=1", "xsort=hot", "scope=ori"]
        self.re_login() if not self.user_uniqueid else 0

        # base class variables
        self.fetch_queue.queue.clear()
        self.saved_set.clear()
        self.current_page = 1
        self.out_file = out_file
        self.out_list = []
        self.out_length = 0

        # this class variables
        self.fetch_keys = fetch_keys
        self.fetch_timescope = fetch_timescope
        self.fetch_type = fetch_type

        # update fetch queue
        self.update_fetch_queue()

        while self.fetch_queue.qsize() > 0:
            url, keys, repeat = self.fetch_queue.get()
            logging.debug("WeiBoSearch: keys=%s, repeat=%s, url=%s", keys, repeat, url)

            try:
                html_all = spider.get_html_content(self.opener.open(url))
                for sc in re.findall("<script>[\w\W]+?STK\.pageletM\.view\(([\w\W]+?)\)</script>", html_all):
                    json_data = json.loads(sc)

                    if json_data.get("pid") == "pl_common_sassfilter":
                        self.check_anti_by_captcha(json_data["html"])
                        self.update_fetch_queue()
                        break

                    if json_data.get("pid") == "pl_weibo_direct":
                        self.parse_search_weibo_page(json_data["html"])
                        break
            except Exception as excep:
                if repeat < self.max_repeat:
                    self.fetch_queue.put(item=(url, keys, repeat+1))
                else:
                    logging.error("WeiBoSearch error: %s, url=%s", excep, url)
        return

    def parse_search_weibo_page(self, html):
        """
        parse search weibo page
        """
        soup = bs4.BeautifulSoup(html, "html.parser")

        if soup.find("div", class_="search_noresult"):
            logging.warning("WeiBoSearch: no result")
            return

        for item in soup.find_all("div", attrs={"action-type": "feed_list_item", "mid": True}):
            weibo_id = item.get("mid")

            soup_info = item.find("a", class_="W_textb", date=True)
            weibo_url = soup_info.get("href")
            weibo_date = datetime.datetime.fromtimestamp(int(soup_info.get("date")) / 1000.0)
            weibo_content = spider.get_string_strip(item.find("p", class_="comment_txt").get_text())

            soup_user = item.find("img", class_="W_face_radius")
            weibo_user = soup_user.get("alt")
            _, querys = spider.get_url_params("http://xxx.com/?" + soup_user.get("usercard"))
            weibo_user_id = querys["id"] if "id" in querys else ""

            weibo_list = (weibo_id, weibo_url, weibo_date, weibo_user_id, weibo_user, weibo_content)
            if self.out_file:
                self.out_file.write("\t".join(map(str, weibo_list)) + "\n")
            else:
                self.out_list.append(weibo_list)
            self.out_length += 1
        logging.debug("WeiBoSearch: current_page=%s, out_length=%s", self.current_page, self.out_length)

        if soup.find("a", class_="page next S_txt1 S_line1", href=True):
            self.current_page += 1
            self.update_fetch_queue()
        return

    def check_anti_by_captcha(self, html):
        """
        check anti-spider by captcha
        """
        soup = bs4.BeautifulSoup(html, "html.parser")

        cid, code = None, None
        while not code:
            captcha_url = soup.find("img", attrs={"node-type": "yzm_img"}).get("src")
            response = self.opener.open(spider.get_url_legal(captcha_url, self.search_url))
            cid, code = self.yundama.get_captcha(response.read(), "captcha.jpeg", "image/jpeg", codetype="1004")

        verified_url = "http://s.weibo.com/ajax/pincode/verified?__rnd=%d" % int(time.time() * 1000)
        post_data = spider.make_post_data({
            "secode": code,
            "type": "sass",
            "pageid": "weibo",
            "_t": 0
        })
        temp = json.loads(spider.get_html_content(self.opener.open(verified_url, data=post_data)))
        if temp["code"] == "100000":
            logging.warning("WeiBoSearch anti-spider succeed")
        else:
            logging.warning("WeiBoSearch anti-spider failed")
            self.yundama.report(cid) if cid else 0
        return
