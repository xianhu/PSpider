# _*_ coding: utf-8 _*_

"""
test.py
"""

import re
import sys
import spider
import logging
import datetime
import requests
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()


class MyFetcher(spider.Fetcher):
    """
    重写spider.Fetcher类，可自定义初始化函数，且必须重写父类中的url_fetch函数
    """

    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):
        """
        定义抓取函数，注意参见父类中对应函数的参数和返回值说明
        """
        response = requests.get(url, proxies=proxies, verify=False, allow_redirects=True, timeout=(3.05, 10))
        return 1, (response.status_code, response.url, response.text), 1


class MyParser(spider.Parser):
    """
    重写spider.Parser类，可自定义初始化函数，且必须重写父类中的htm_parse函数
    """

    def __init__(self, max_deep=0):
        """
        初始化函数，构建一个新变量_max_deep
        """
        spider.Parser.__init__(self)
        self._max_deep = max_deep
        return

    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        """
        定义解析函数，解析抓取到的content，生成待抓取的url和待保存的item
        """
        status_code, url_now, html_text = content

        url_list = []
        if (self._max_deep < 0) or (deep < self._max_deep):
            re_group = re.findall(r"<a.+?href=\"(?P<url>.{5,}?)\".*?>", html_text, flags=re.IGNORECASE)
            url_list = [(spider.get_url_legal(_url, base_url=url), keys, priority + 1) for _url in re_group]

        title = re.search(r"<title>(?P<title>.+?)</title>", html_text, flags=re.IGNORECASE)
        item = {"url": url, "title": title.group("title").strip(), "datetime": datetime.datetime.now()} if title else {}

        return 1, url_list, item


class MySaver(spider.Saver):
    """
    重写spider.Saver类，可自定义初始化函数，且必须重写父类中的item_save函数
    """

    def __init__(self, save_pipe=sys.stdout):
        """
        初始化函数
        """
        spider.Saver.__init__(self)
        self._save_pipe = save_pipe
        return

    def item_save(self, priority: int, url: str, keys: dict, deep: int, item: dict):
        """
        定义保存函数，将item保存到本地文件或者数据库
        """
        self._save_pipe.write("\t".join([item["url"], item["title"], str(item["datetime"])]) + "\n")
        self._save_pipe.flush()
        return 1, None


class MyProxies(spider.Proxieser):
    """
    重写spider.Proxieser类，可自定义初始化函数，且必须重写父类中的proxies_get函数
    """

    def proxies_get(self):
        """
        获取代理，并返回给线程池，推荐使用快代理
        """
        response = requests.get("http://xxxx.com/proxies")
        proxies_list = [{"http": "http://%s" % ipport, "https": "https://%s" % ipport} for ipport in response.text.split("\n")]
        return 1, proxies_list


def test_spider():
    """
    测试函数
    """
    # 初始化 fetcher / parser / saver / proxieser
    fetcher = MyFetcher(sleep_time=0, max_repeat=3)
    parser = MyParser(max_deep=1)
    saver = MySaver(save_pipe=open("out.txt", "w"))
    # proxieser = MyProxies(sleep_time=5)

    # 定义url_filter
    url_filter = spider.UrlFilter(white_patterns=(re.compile(r"^http[s]?://www\.appinn\.com"),))

    # 定义爬虫web_spider
    web_spider = spider.WebSpider(fetcher, parser, saver, proxieser=None, url_filter=url_filter, queue_parse_size=-1, queue_save_size=-1)
    # web_spider = spider.WebSpider(fetcher, parser, saver, proxieser=proxieser, url_filter=url_filter, queue_parse_size=100, queue_proxies_size=100)

    # 添加起始的url
    web_spider.set_start_url("https://www.appinn.com/", priority=0, keys={"type": "index"}, deep=0, repeat=0)

    # 开启爬虫web_spider
    web_spider.start_working(fetchers_num=10)

    # 等待爬虫结束
    web_spider.wait_for_finished()
    return


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")
    test_spider()
