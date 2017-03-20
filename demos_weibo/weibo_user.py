# _*_ coding: utf-8 _*_

import re
import bs4
import sys
import json
import time
import spider
import random
import logging
import datetime
import urllib.parse
from .weibo_login import WeiBoBase


class WeiBoUser(WeiBoBase):
    """
    class of WeiBoUser
    """

    def __init__(self, users_pair):
        """
        constructor
        """
        WeiBoBase.__init__(self, users_pair=users_pair)

        # parameters which are needed in this class
        self.bar_url = "http://weibo.com/p/aj/v6/mblog/mbloglist?"
        self.html_re = re.compile("<script>FM\.view\(([\w\W]+?)\);*</script>")
        return

    def fetch_user_from_id(self, user_id):
        """
        fetch user data from user_id
        :return user_name, [user_page_follows, user_page_fans, user_page_weibos], [follows, fans, weibos]
        """
        self.re_login() if not self.user_uniqueid else 0

        user_url_base = "http://weibo.com/%s/profile" % user_id.strip()
        user_name, user_pages, user_counts = None, [], []

        repeat_time = 0
        while repeat_time <= self.max_repeat:
            logging.debug("WeiBoUser repeat: repeat_time=%d" % repeat_time) if repeat_time > 0 else 0
            html_all = spider.get_html_content(self.opener.open(user_url_base, timeout=5))

            header_dict = {key: value for key, value in self.header_re.findall(html_all)}
            if ("uid" not in header_dict) or ("nick" not in header_dict):
                repeat_time += 1
                continue

            if ("onick" not in header_dict) or (header_dict["onick"] == header_dict["nick"]):
                repeat_time += 1
                continue

            for sc_string in self.html_re.findall(html_all):
                json_data = json.loads(sc_string)
                if json_data["domid"] == "Pl_Core_T8CustomTriColumn__3" and "html" in json_data:
                    soup = bs4.BeautifulSoup(json_data["html"], "html.parser")
                    a_soup_list = soup.find_all("a", class_="S_txt1")
                    user_pages = [a_soup.get("href") for a_soup in a_soup_list]
                    user_counts = [int(spider.get_string_num(a_soup.get_text())) for a_soup in a_soup_list]
                    user_name = header_dict["onick"]
                    break

            if user_name:
                break

            repeat_time += 1
        # return result
        logging.warning("WeiBoUser fetch_user_from_id: user_id=%s, user_name=%s" % (user_id, user_name))
        return user_name, user_pages, user_counts

    def fetch_user_weibos(self, user_url, key_dict, file_out=sys.stdout, sleep_time=0):
        """
        fetch user weibo, user_url like: http://weibo.com/p/1005051750270991/home?parameters
        :param key_dict: {"mod": "data", "is_all": 1}
        :param key_dict: {"stat_date": "201512", "is_all": 1}
        :param key_dict: {
            "is_ori": 1, "is_forward": 1, "is_text": 1, "is_pic": 1, "is_video": 1, "is_music": 1, "is_article": 1,
            "key_word": "a b", "start_time": "2016-06-01", "end_time": "2016-06-04", "is_search": 1, "is_searchadv": 1
        }
        """
        self.re_login() if not self.user_uniqueid else 0

        self.fetch_queue.queue.clear()
        self.current_page = 1
        self.file_out = file_out

        # get the start url
        url_main, _ = spider.get_url_params(user_url, is_unique_values=True)
        self.fetch_queue.put((url_main+"?"+urllib.parse.urlencode(key_dict), "page_index", 0))

        # get data from url
        while self.fetch_queue.qsize() > 0:
            time.sleep(random.randint(0, sleep_time)) if sleep_time > 0 else 0
            url, keys, repeat = self.fetch_queue.get()

            try:
                html_all = spider.get_html_content(self.opener.open(url, timeout=5))
                main, querys = spider.get_url_params(url, is_unique_values=True)

                if keys == "page_index":
                    logging.warning("WeiBoUser index: repeat=%d, page=%d, url=%s" % (repeat, self.current_page, url))

                    header_dict = {key: value for key, value in self.header_re.findall(html_all)}
                    for sc_string in self.html_re.findall(html_all):
                        json_data = json.loads(sc_string)
                        if json_data.get("ns") == "pl.content.homeFeed.index" and \
                                json_data["domid"].startswith("Pl_Official_MyProfileFeed"):
                            # get index data
                            weibo_count, is_loading, next_page = self.parse_user_weibo_page(json_data["html"])
                            if is_loading:
                                # pagebar 0 and 1
                                post_dict = {
                                    "id": querys.get("id", header_dict["page_id"]),
                                    "domain": querys.get("domain", header_dict["domain"]),
                                    "domain_op": querys.get("domain_op", header_dict["domain"]),
                                    "pre_page": querys.get("page", 1),
                                    "page": querys.get("page", 1),
                                    "pagebar": 0,
                                    "feed_type": 0,
                                    "ajwvr": 6,
                                    "__rnd": int(time.time() * 1000)
                                }
                                post_dict.update(key_dict)
                                self.fetch_queue.put((self.bar_url+urllib.parse.urlencode(post_dict), "page_bar", 0))
                            break

                elif keys == "page_bar":
                    logging.warning("WeiBoUser bar=%s: page=%d url=%s" % (querys["pagebar"], self.current_page, url))

                    # get bar data
                    weibo_count, is_loading, next_page = self.parse_user_weibo_page(json.loads(html_all)["data"])
                    if is_loading:
                        querys["pagebar"] = 1
                        self.fetch_queue.put((self.bar_url+urllib.parse.urlencode(querys), "page_bar", 0))

                    if next_page:
                        self.current_page += 1
                        _temp = next_page.get("href")
                        self.fetch_queue.put((url_main+_temp[_temp.find("?"):], "page_index", 0))

            except Exception as e:
                if repeat < self.max_repeat:
                    self.fetch_queue.put((url, keys, repeat+1))
                else:
                    logging.error("WeiBoUser error: error=%s, url=%s" % (str(e), url))
        return

    def parse_user_weibo_page(self, html):
        """
        parse user weibo page, return weibo_count, is_loading, next_page_soup
        """
        # check frequence
        if html.find("你搜的太频繁了") > 0:
            logging.warning("WeiBoUser frequence warning: re_login!")
            self.re_login()
            assert False

        soup = bs4.BeautifulSoup(html, "html.parser")
        weibo_count, is_loading, next_page_soup = 0, False, soup.find("a", class_="page next S_txt1 S_line1")

        # check weibo number
        count_soup = soup.find("em", class_="W_fb S_spetxt")
        if (not count_soup) or int(count_soup.get_text()) > 0:
            for weibo_soup in soup.find_all("div", class_=re.compile("WB_cardwrap"), mid=True):
                weibo_count += 1

                weibo_id = weibo_soup.get("mid")
                if weibo_id in self.saved_set:
                    continue

                # user information -- user_name and user_href
                user_div = weibo_soup.find("div", class_="WB_info")
                user_name = user_div.find("a", usercard=True).get_text()
                assert user_name, "WeiBoUser error: user_name is null!"

                # content information -- content_date
                date_div = weibo_soup.find("div", class_="WB_from S_txt2")
                content_date = datetime.datetime.fromtimestamp(int(date_div.find("a", date=True).get("date")) / 1000.0)

                # content information -- content and expand_users
                content_div = weibo_soup.find("div", class_="WB_text W_f14")
                content = spider.get_string_strip(content_div.get_text())
                self.file_out.write("\t".join([user_name, str(content_date), content]) + "\n")

                # expand information
                expand_weibo = weibo_soup.find("div", class_="WB_feed_expand")
                if expand_weibo and (not expand_weibo.find("div", class_="WB_empty")):
                    expand_user_div = expand_weibo.find("div", class_="WB_info")
                    expand_user_name = expand_user_div.find("a", usercard=True).get_text().strip("@")

                    # expand_date_div = expand_weibo.find("div", class_="WB_from S_txt2")
                    expand_content = spider.get_string_strip(expand_weibo.find("div", class_="WB_text").get_text())
                    self.file_out.write("\t".join([user_name, "ex_c", expand_user_name, expand_content]) + "\n")

                self.saved_set.add(weibo_id)
            # if is_loading
            is_loading = True if html.rfind("正在加载中") > 0 else False

        logging.debug("WeiBoUser: weibo_count=%d, weibo_all=%d, is_loading=%s, next_page=%s" %
                      (weibo_count, len(self.saved_set), str(is_loading), str(bool(next_page_soup))))
        return weibo_count, is_loading, next_page_soup
