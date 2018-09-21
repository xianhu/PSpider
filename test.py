# _*_ coding: utf-8 _*_

"""
test.py by xianhu
"""

import re
import spider
import logging
import datetime
import requests

black_patterns = (spider.CONFIG_URL_ILLEGAL_PATTERN, r"binding", r"download", )
white_patterns = (r"^http[s]{0,1}://(www\.){0,1}(zhushou\.360)\.(com|cn)", )


class MyFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):
        response = requests.get(url, params=None, headers={}, data=None, proxies=proxies, timeout=(3.05, 10))
        content = (response.status_code, response.url, response.text)
        return 1, True, content


class MyParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        status_code, url_now, html_text = content

        url_list = []
        if (self._max_deep < 0) or (deep < self._max_deep):
            tmp_list = re.findall(r"<a.+?href=\"(?P<url>.{5,}?)\".*?>", html_text, flags=re.IGNORECASE)
            url_list = [(_url, keys, priority+1) for _url in [spider.get_url_legal(href, url) for href in tmp_list]]

        title = re.search(r"<title>(?P<title>.+?)</title>", html_text, flags=re.IGNORECASE)
        save_list = [(url, title.group("title").strip(), datetime.datetime.now()), ] if title else []

        return 1, url_list, save_list


def test_spider():
    """
    test spider
    """
    # initial fetcher / parser / saver
    fetcher = MyFetcher(max_repeat=3, sleep_time=1)
    parser = MyParser(max_deep=1)
    saver = spider.Saver(save_pipe=open("out_thread.txt", "w"))

    # define url_filter
    url_filter = spider.UrlFilter(black_patterns=black_patterns, white_patterns=white_patterns, capacity=None)

    # initial web_spider
    web_spider = spider.WebSpider(fetcher, parser, saver, proxieser=None, url_filter=url_filter, max_count_in_fetch=500, max_count_in_proxies=100)

    # add start url
    web_spider.set_start_url("http://zhushou.360.cn/", priority=0, keys={"type": "360"}, deep=0)

    # start web_spider
    web_spider.start_working(fetcher_num=10)

    # wait for finished
    web_spider.wait_for_finished()
    return


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")
    test_spider()
    exit()
