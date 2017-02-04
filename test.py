# _*_ coding: utf-8 _*_

"""
test.py by xianhu
"""

import spider
import asyncio
import logging


def test_spider():
    """
    test spider
    """
    # 定义fetcher, parser和saver, 你也可以重写这三个类中的任何一个
    fetcher = spider.Fetcher(max_repeat=3, sleep_time=0)
    parser = spider.Parser(max_deep=1)
    saver = spider.Saver(save_pipe=open("out_spider_thread.txt", "w"))

    # 定义Url过滤, UrlFilter使用Set, 适合Url数量不多的情况
    black_patterns = (spider.CONFIG_URLPATTERN_FILES, r"binding", r"download", )
    white_patterns = ("^http[s]{0,1}://(www\.){0,1}(wandoujia|(zhushou\.360))\.(com|cn)", )
    url_filter = spider.UrlFilter(black_patterns=black_patterns, white_patterns=white_patterns, capacity=1000)
    # url_filter.update([])

    # 初始化WebSpider
    web_spider = spider.WebSpider(fetcher, parser, saver, url_filter=url_filter, monitor_sleep_time=5)

    # 添加种子Url
    web_spider.set_start_url("http://zhushou.360.cn/", keys=("360web",))

    # 开始抓取任务并等待其结束
    web_spider.start_work_and_wait_done(fetcher_num=10)
    return


def test_spider_async():
    """
    test spider with asyncio
    """
    # 得到Loop
    loop = asyncio.get_event_loop()

    # 定义fetcher, parser和saver, 你也可以重写这三个类中的任何一个
    fetcher = spider.FetcherAsync(max_repeat=3, sleep_time=0)
    parser = spider.ParserAsync(max_deep=1)
    saver = spider.SaverAsync(save_pipe=open("out_spider_async.txt", "w"))

    # 初始化WebSpiderAsync
    web_spider_async = spider.WebSpiderAsync(fetcher, parser, saver, url_filter=spider.UrlFilter(), loop=loop)

    # 添加种子Url
    web_spider_async.set_start_url("http://zhushou.360.cn/", keys=("360web",))

    # 开始抓取任务并等待其结束
    web_spider_async.start_work_and_wait_done(fetcher_num=10)
    return


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")
    test_spider()
    test_spider_async()
    exit()
