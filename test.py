# _*_ coding: utf-8 _*_

"""
test.py by xianhu
"""

import re
import spider
import random
import datetime
import requests
from bs4 import BeautifulSoup

black_patterns = (spider.CONFIG_URL_ILLEGAL_PATTERN, r"binding", r"download", )
white_patterns = (r"^http[s]{0,1}://(www\.){0,1}(zhushou\.360)\.(com|cn)", )


class MyFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):
        response = requests.get(url, params=None, headers={}, data=None, proxies=proxies, timeout=(3.05, 10))
        result = (response.status_code, response.url, response.text)

        # test error-logging
        assert random.randint(0, 100) != 8, "error-in-fetcher"
        return 1, result, 1


class MyParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        status_code, url_now, html_text = content
        # test multi-processing
        [BeautifulSoup(html_text, "lxml") for _ in range(10)]

        url_list = []
        if (self._max_deep < 0) or (deep < self._max_deep):
            re_group = re.findall(r"<a.+?href=\"(?P<url>.{5,}?)\".*?>", html_text, flags=re.IGNORECASE)
            url_list = [(spider.get_url_legal(_url, base_url=url), keys, priority+1) for _url in re_group]

        title = re.search(r"<title>(?P<title>.+?)</title>", html_text, flags=re.IGNORECASE)
        save_list = [(url, title.group("title").strip(), datetime.datetime.now()), ] if title else []

        # test error-logging
        assert random.randint(0, 100) != 8, "error-in-parser"
        return 1, url_list, save_list


class MySaver(spider.Saver):
    """
    saver module, only rewrite item_save()
    """
    def item_save(self, url: str, keys: dict, item: (list, tuple)):
        self._save_pipe.write("\t".join([str(col) for col in item] + [url, ]) + "\n")
        self._save_pipe.flush()
        return 1, []


class MyProxies(spider.Proxieser):
    """
    proxies module, only rewrite proxies_get()
    """
    def proxies_get(self):
        response = requests.get("http://xxxx.com/proxies")
        proxies_result = [{"http": "http://%s" % ipport, "https": "https://%s" % ipport} for ipport in response.text.split("\n")]
        return 1, proxies_result


def test_spider():
    """
    test spider
    """
    # initial fetcher / parser / saver / proxieser
    fetcher = MyFetcher(sleep_time=1, max_repeat=0)
    parser = MyParser(max_deep=2)
    saver = MySaver(save_pipe=open("out_thread.txt", "w"))
    # proxieser = MyProxies(sleep_time=5)

    # define url_filter
    url_filter = spider.UrlFilter(black_patterns=black_patterns, white_patterns=white_patterns, capacity=None)

    # initial web_spider
    # web_spider = spider.WebSpider(fetcher, parser, saver, proxieser=None, url_filter=url_filter, queue_parse_size=-1)
    web_spider = spider.WebSpider(fetcher, parser, saver, proxieser=None, url_filter=url_filter, queue_parse_size=100, queue_proxies_size=100)

    # add start url
    web_spider.set_start_url("http://zhushou.360.cn/", priority=0, keys={"type": "360"}, deep=0)

    # start web_spider
    web_spider.start_working(fetcher_num=20)

    # wait for finished
    web_spider.wait_for_finished()
    return


if __name__ == "__main__":
    test_spider()
    exit()
