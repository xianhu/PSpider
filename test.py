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


class MyFetcher(spider.Fetcher):
    """
    重写spider.Fetcher类，可自定义初始化函数，且必须重写父类中的url_fetch函数
    """

    def url_fetch(self, task_fetch, proxies=None) -> spider.ResultFetch:
        """
        定义抓取函数，注意参见父类中对应函数的参数和返回值说明
        """
        response = requests.get(task_fetch.url, proxies=proxies, allow_redirects=True, timeout=(3.05, 10))
        content = (response.status_code, response.url, response.text)
        task_parse = spider.TaskParse(content=content, task_fetch=task_fetch)
        return spider.ResultFetch(state_code=1, state_proxies=1, task_parse=task_parse)


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

    def htm_parse(self, task_parse) -> spider.ResultParse:
        """
        定义解析函数，解析抓取到的content，生成待抓取的url和待保存的item
        """
        status_code, url_now, html_text = task_parse.content

        task_fetch_list = []
        if (self._max_deep < 0) or (task_parse.deep < self._max_deep):
            re_group = re.findall(r"<a.+?href=\"(?P<url>.{5,}?)\".*?>", html_text, flags=re.IGNORECASE)
            url_list = [spider.get_url_legal(_url, base_url=task_parse.url) for _url in re_group]
            task_fetch_list = [spider.TaskFetch(priority=task_parse.priority + 1, keys=task_parse.keys, deep=task_parse.deep + 1, url=_url) for _url in url_list]

        title = re.search(r"<title>(?P<title>.+?)</title>", html_text, flags=re.IGNORECASE)
        item = {"url": task_parse.url, "title": title.group("title").strip(), "datetime": datetime.datetime.now()} if title else {}

        return spider.ResultParse(state_code=1, task_fetch_list=task_fetch_list, task_save=spider.TaskSave(item=item, task_parse=task_parse))


class MySaver(spider.Saver):
    """
    重写spider.Saver类，可自定义初始化函数，且必须重写父类中的item_save函数
    """

    def __init__(self, save_pipe=sys.stdout):
        """
        初始化函数，构建一个新变量_save_pipe
        """
        spider.Saver.__init__(self)
        self._save_pipe = save_pipe
        return

    def item_save(self, task_save):
        """
        定义保存函数，将item保存到本地文件或者数据库
        """
        self._save_pipe.write("\t".join([task_save.item["url"], task_save.item["title"], str(task_save.item["datetime"])]) + "\n")
        self._save_pipe.flush()
        return spider.ResultSave(state_code=1)


class MyProxies(spider.Proxieser):
    """
    重写spider.Proxieser类，可自定义初始化函数，且必须重写父类中的proxies_get函数
    """

    def proxies_get(self):
        """
        获取代理，并返回给线程池，推荐使用快代理
        """
        response = requests.get("https://xxxx.com/proxies")
        proxies_list = [{"https": "https://%s" % ipport} for ipport in response.text.split("\n")]
        return spider.ResultProxies(state_code=1, proxies_list=proxies_list)


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
    url_filter = spider.UrlFilter(white_patterns=(re.compile(r"^https?://www\.appinn\.com"),))

    # 定义爬虫web_spider
    web_spider = spider.WebSpider(fetcher, parser, saver, proxieser=None, url_filter=url_filter, queue_parse_size=-1, queue_save_size=-1)
    # web_spider = spider.WebSpider(fetcher, parser, saver, proxieser=proxieser, url_filter=url_filter, queue_parse_size=100, queue_proxies_size=100)

    # 添加起始的url
    url = "https://www.appinn.com/"
    web_spider.set_start_task(spider.TaskFetch(priority=0, keys={"type": "index"}, deep=0, url=url))

    # 开启爬虫web_spider
    web_spider.start_working(fetchers_num=2)

    # 等待爬虫结束
    web_spider.wait_for_finished()
    return


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")
    test_spider()
