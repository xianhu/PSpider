# _*_ coding: utf-8 _*_

"""
test.py by xianhu
"""

import spider
import logging
logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")


def test_spider(spider_type):
    """
    test spider
    """
    # 定义fetcher,parser和saver, 你也可以重写这三个类中的任何一个
    fetcher = spider.Fetcher(normal_max_repeat=3, normal_sleep_time=0, critical_max_repeat=5, critical_sleep_time=5)
    parser = spider.Parser(max_deep=1, max_repeat=2)
    saver = spider.Saver(file_name="out_%s.txt" % spider_type)

    # 定义Url过滤, UrlFilter使用Set, 适合Url数量不多的情况
    black_patterns = (spider.CONFIG_URLPATTERN_FILES, r"binding", r"download", )
    white_patterns = ("^http[s]{0,1}://(www\.){0,1}(wandoujia|(zhushou\.360))\.(com|cn)", )
    url_filter = spider.UrlFilter(black_patterns=black_patterns, white_patterns=white_patterns, capacity=None)

    # 确定使用ThreadPool还是ProcessPool
    web_spider = spider.WebSpider(fetcher, parser, saver, url_filter=url_filter, monitor_sleep_time=5, pool_type=spider_type)
    parser_num = 1 if spider_type == "thread" else 3

    # 首先抓取一次豌豆荚页面, 抓取完成之后不停止monitor
    web_spider.set_start_url("http://www.wandoujia.com/apps", ("wandoujia",), priority=0, deep=0, critical=False)
    web_spider.start_work_and_wait_done(fetcher_num=10, parser_num=parser_num, is_over=False)

    # 然后抓取360应用商店页面, 抓取完成之后停止monitor
    web_spider.set_start_url("http://zhushou.360.cn/", ("360app",), priority=0, deep=0, critical=False)
    web_spider.start_work_and_wait_done(fetcher_num=10, parser_num=parser_num, is_over=True)
    return


if __name__ == "__main__":
    # 测试多线程抓取
    test_spider(spider_type="thread")

    # 测试多线程/多进程混合抓取, 在Windows上可能有问题
    # test_spider(spider_type="process")
    exit()
