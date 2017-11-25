# _*_ coding: utf-8 _*_

"""
test.py by xianhu
"""

import spider
import logging

black_patterns = (spider.CONFIG_URL_PATTERN, r"binding", r"download",)
white_patterns = (r"^http[s]{0,1}://(www\.){0,1}(zhushou\.360)\.(com|cn)",)


def test_spider():
    """
    test spider
    """
    # initial fetcher / parser / saver, you also can rewrite this three class
    fetcher = spider.Fetcher(max_repeat=1, sleep_time=0)
    parser = spider.Parser(max_deep=2)
    saver = spider.Saver(save_pipe=open("out_spider_thread.txt", "w"))

    # define url_filter
    url_filter = spider.UrlFilter(black_patterns=black_patterns, white_patterns=white_patterns, capacity=None)

    # initial web_spider
    web_spider = spider.WebSpider(fetcher, parser, saver, url_filter=url_filter, monitor_sleep_time=5)
    # web_spider = spider.WebSpider(fetcher, parser, saver, url_filter=url_filter, proxies_func=proxies_func, monitor_sleep_time=5)

    # add start url
    web_spider.set_start_url("http://zhushou.360.cn/", priority=0, keys="360web", deep=0)

    # start web_spider
    web_spider.start_work_and_wait_done(fetcher_num=10, is_over=True)
    return


def test_spider_distributed():
    """
    test distributed spider
    """
    # initial fetcher / parser / saver, you also can rewrite this three class
    fetcher = spider.Fetcher(max_repeat=1, sleep_time=0)
    parser = spider.Parser(max_deep=-1)
    saver = spider.Saver(save_pipe=open("out_spider_distributed.txt", "w"))

    # define url_filter
    url_filter = spider.UrlFilter(black_patterns=black_patterns, white_patterns=white_patterns)

    # initial web_spider
    web_spider_dist = spider.WebSpiderDist(fetcher, parser, saver, url_filter=url_filter, monitor_sleep_time=5)
    web_spider_dist.init_redis(host="localhost", port=6379, key_high_priority="spider.high", key_low_priority="spider.low")

    # start web_spider
    web_spider_dist.start_work_and_wait_done(fetcher_num=10)
    return


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")
    test_spider()
    # test_spider_distributed()
    exit()
