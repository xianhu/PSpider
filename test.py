# _*_ coding: utf-8 _*_

"""
test.py by xianhu
"""

import spider
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")


def test_spider():
    """
    test spider
    """
    # 定义fetcher,parser和saver, 你也可以重写这三个类中的任何一个
    fetcher = spider.Fetcher(normal_max_repeat=3, normal_sleep_time=0, critical_max_repeat=5, critical_sleep_time=5)
    parser = spider.Parser(max_deep=1, max_repeat=2)
    saver = spider.Saver(save_pipe=open("out_spider.txt", "w"))

    # 定义Url过滤, UrlFilter使用Set, 适合Url数量不多的情况
    black_patterns = (spider.CONFIG_URLPATTERN_FILES, r"binding", r"download", )
    white_patterns = ("^http[s]{0,1}://(www\.){0,1}(wandoujia|(zhushou\.360))\.(com|cn)", )
    url_filter = spider.UrlFilter(black_patterns=black_patterns, white_patterns=white_patterns, capacity=1000)
    url_filter.update([])

    # 初始化WebSpider
    web_spider = spider.WebSpider(fetcher, parser, saver, url_filter=url_filter, monitor_sleep_time=5)

    # 首先抓取一次豌豆荚页面, 抓取完成之后不停止monitor
    web_spider.set_start_url("http://www.wandoujia.com/apps", ("wandoujia",), priority=0, deep=0, critical=False)
    web_spider.start_work_and_wait_done(fetcher_num=10, is_over=False)

    # 然后抓取360应用商店页面, 抓取完成之后停止monitor
    web_spider.set_start_url("http://zhushou.360.cn/", ("360app",), priority=0, deep=0, critical=False)
    web_spider.start_work_and_wait_done(fetcher_num=10, is_over=True)
    return


if __name__ == "__main__":
    test_spider()
    exit()
