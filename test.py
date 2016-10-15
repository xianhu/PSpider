# _*_ coding: utf-8 _*_

"""
test.py by xianhu
"""

import sys
import spider
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")


def test_spider(mysql, spider_type):
    """
    test spider
    """
    # 定义fetcher, parser和saver, 你也可以重写这三个类
    fetcher = spider.Fetcher(normal_max_repeat=3, normal_sleep_time=0, critical_max_repeat=5, critical_sleep_time=5)
    parser = spider.Parser(max_deep=1, max_repeat=3)

    if not mysql:
        saver = spider.Saver(save_pipe=sys.stdout)

        # UrlFilter, 使用Set, 适合Url数量不多的情况
        url_filter = spider.UrlFilter(
            black_patterns=(spider.CONFIG_URLPATTERN_FILES, r"/binding$"),
            white_patterns=("^http[s]{0,1}://(www\.){0,1}(wandoujia|(zhushou\.360)|duba_\d)\.(com|cn)", ),
            capacity=None
        )
    else:
        saver = spider.SaverMysql(host="localhost", user="root", passwd="123456", database="default")
        saver.change_sqlstr("insert into t_test(url, title, getdate) values (%s, %s, %s);")

        # UrlFilter, 使用BloomFilter, 适合Url数量巨大的情况
        url_filter = spider.UrlFilter(
            black_patterns=(spider.CONFIG_URLPATTERN_FILES, r"/binding$"),
            white_patterns=("^http[s]{0,1}://(www\.){0,1}(wandoujia|(zhushou\.360)|duba_\d)\.(com|cn)", ),
            capacity=1000
        )

    # 确定使用ThreadPool还是ProcessPool
    if spider_type == "thread":
        web_spider = spider.WebSpiderT(fetcher, parser, saver, url_filter=url_filter, monitor_sleep_time=5)
    else:
        web_spider = spider.WebSpiderP(fetcher, parser, saver, url_filter=url_filter, monitor_sleep_time=5)

    parser_num = 1 if spider_type == "thread" else 3

    # 首先抓取一次豌豆荚的应用页面,抓取完成之后不停止monitor
    web_spider.set_start_url("http://www.wandoujia.com/apps", ("wandoujia",), priority=0, deep=0, critical=False)
    web_spider.start_work_and_wait_done(fetcher_num=5, parser_num=parser_num, is_over=False)

    # 然后抓取360应用商店的应用页面,并试验critical参数的作用,抓取完成之后停止monitor
    web_spider.set_start_url("http://zhushou.360.cn/", ("360app",), priority=0, deep=0, critical=False)
    for i in range(5):
        web_spider.set_start_url("https://www.duba_%d.com/" % i, ("critical",), priority=0, deep=0, critical=True)
    web_spider.start_work_and_wait_done(fetcher_num=5, parser_num=parser_num, is_over=True)

    return


if __name__ == '__main__':
    # 测试多线程抓取
    # test_spider(mysql=False, spider_type="thread")
    test_spider(mysql=True, spider_type="thread")

    # 测试多线程/多进程混合抓取
    # test_spider(mysql=False, spider_type="process")
    test_spider(mysql=True, spider_type="process")
    exit()
