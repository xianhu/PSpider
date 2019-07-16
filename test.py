# _*_ coding: utf-8 _*_

"""
test.py by xianhu
"""

import re
import sys
import spider
import random
import logging
import datetime
import requests
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()


class MyFetcher(spider.Fetcher):
    """
    fetcher module, rewrite url_fetch()
    """

    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):
        # test error-logging
        assert random.randint(0, 100) != 8, "error-in-fetcher"

        response = requests.get(url, params=None, headers={}, data=None, proxies=proxies, verify=False, allow_redirects=True, timeout=(3.05, 10))
        response.raise_for_status()
        return 1, (response.status_code, response.url, response.text), 1


class MyParser(spider.Parser):
    """
    parser module, rewrite htm_parse()
    """

    def __init__(self, max_deep=0):
        """
        constructor
        """
        spider.Parser.__init__(self)
        self._max_deep = max_deep
        return

    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        # test error-logging
        assert random.randint(0, 100) != 8, "error-in-parser"

        status_code, url_now, html_text = content

        url_list = []
        if (self._max_deep < 0) or (deep < self._max_deep):
            re_group = re.findall(r"<a.+?href=\"(?P<url>.{5,}?)\".*?>", html_text, flags=re.IGNORECASE)
            url_list = [(spider.get_url_legal(_url, base_url=url), keys, priority+1) for _url in re_group]

        # save_list can be list / tuple / dict
        title = re.search(r"<title>(?P<title>.+?)</title>", html_text, flags=re.IGNORECASE)
        # item = (url, title.group("title").strip(), datetime.datetime.now()) if title else []
        item = {"url": url, "title": title.group("title").strip(), "datetime": datetime.datetime.now()} if title else {}

        # test multi-processing(heavy time)
        [BeautifulSoup(html_text, "lxml") for _ in range(10)]
        return 1, url_list, item


class MySaver(spider.Saver):
    """
    saver module, rewrite item_save()
    """
    def __init__(self, save_pipe=sys.stdout):
        """
        constructor
        """
        spider.Saver.__init__(self)
        self._save_pipe = save_pipe
        return

    def item_save(self, priority: int, url: str, keys: dict, deep: int, item: object):
        # test error-logging
        assert random.randint(0, 100) != 8, "error-in-saver"

        # item can be list / tuple / dict
        # self._save_pipe.write("\t".join([str(col) for col in item]) + "\n")
        self._save_pipe.write("\t".join([item["url"], item["title"], str(item["datetime"])]) + "\n")
        self._save_pipe.flush()
        return 1, None


class MyProxies(spider.Proxieser):
    """
    proxies module, only rewrite proxies_get()
    """
    def proxies_get(self):
        response = requests.get("http://xxxx.com/proxies")
        proxies_list = [{"http": "http://%s" % ipport, "https": "https://%s" % ipport} for ipport in response.text.split("\n")]
        return 1, proxies_list


def test_spider():
    """
    test spider
    """
    # initial fetcher / parser / saver / proxieser
    fetcher = MyFetcher(sleep_time=0, max_repeat=1)
    parser = MyParser(max_deep=1)
    saver = MySaver(save_pipe=open("out.txt", "w"))
    # proxieser = MyProxies(sleep_time=5)

    # define url_filter
    url_filter = spider.UrlFilter(white_patterns=(re.compile(r"^http[s]?://(www\.)?appinn\.com"), ), capacity=None)

    # initial web_spider
    web_spider = spider.WebSpider(fetcher, parser, saver, proxieser=None, url_filter=url_filter, queue_parse_size=-1, queue_save_size=-1)
    # web_spider = spider.WebSpider(fetcher, parser, saver, proxieser=proxieser, url_filter=url_filter, queue_parse_size=100, queue_proxies_size=100)

    # add start url
    web_spider.set_start_url("https://www.appinn.com/", priority=0, keys={"type": "index"}, deep=0)

    # start web_spider
    web_spider.start_working(fetcher_num=20)

    # wait for finished
    web_spider.wait_for_finished()
    return


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")
    test_spider()
