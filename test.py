# _*_ coding: utf-8 _*_

"""
test.py by xianhu
"""

import re
import random
import logging
import datetime
import spider
logging.basicConfig(level=logging.WARNING, format="%(asctime)s\t%(levelname)s\t%(message)s")


# 继承并重写Parser类
class MyParser(spider.Parser):

    def htm_parse(self, priority, url, keys, deep, critical, parse_repeat, content):
        """
        重写函数htm_parse()
        """
        # parse content (cur_code, cur_url, cur_info, cur_html)
        *_, cur_html = content
        cur_html = cur_html.decode("utf-8")

        # get url_list and save_list
        url_list = []
        if (self.max_deep < 0) or (deep < self.max_deep):
            a_list = re.findall(r"<a[\w\W]+?href=\"(?P<url>[\w\W]+?)\"[\w\W]*?>[\w\W]+?</a>", cur_html, flags=re.IGNORECASE)
            url_list = [(_url, keys, critical, priority+1) for _url in [spider.get_url_legal(href, url) for href in a_list]]
        title = re.search(r"<title>(?P<title>[\w\W]+?)</title>", cur_html, flags=re.IGNORECASE)
        save_list = [(url, title.group("title"), datetime.datetime.now()), ] if title else []

        # test cpu task
        count = 0
        for i in range(1000):
            for j in range(1000):
                count += ((i*j) / 1000)

        # test parsing error
        if random.randint(0, 5) == 3:
            parse_repeat += (1 / 0)

        # return code, url_list, save_list
        return 1, url_list, save_list


def test_spider(spider_type):
    """
    test spider
    """
    # 定义fetcher,parser和saver, 你也可以重写这三个类中的任何一个
    fetcher = spider.Fetcher(normal_max_repeat=3, normal_sleep_time=0, critical_max_repeat=5, critical_sleep_time=5)
    parser = spider.Parser(max_deep=1, max_repeat=2)
    # parser = MyParser(max_deep=1, max_repeat=2)
    saver = spider.Saver(file_name="out_%s.txt" % spider_type)

    # 定义Url过滤, UrlFilter使用Set, 适合Url数量不多的情况
    black_patterns = (spider.CONFIG_URLPATTERN_FILES, r"binding", r"download", )
    white_patterns = ("^http[s]{0,1}://(www\.){0,1}(wandoujia|(zhushou\.360))\.(com|cn)", )
    url_filter = spider.UrlFilter(black_patterns=black_patterns, white_patterns=white_patterns, capacity=None)

    # 确定使用ThreadPool还是ProcessPool
    if spider_type == "thread":
        web_spider = spider.WebSpiderT(fetcher, parser, saver, url_filter=url_filter, monitor_sleep_time=5)
    else:
        web_spider = spider.WebSpiderP(fetcher, parser, saver, url_filter=url_filter, monitor_sleep_time=5)

    parser_num = 1 if spider_type == "thread" else 3

    # 首先抓取一次豌豆荚页面,抓取完成之后不停止monitor
    web_spider.set_start_url("http://www.wandoujia.com/apps", ("wandoujia",), priority=0, deep=0, critical=False)
    web_spider.start_work_and_wait_done(fetcher_num=10, parser_num=parser_num, is_over=False)

    # 然后抓取360应用商店页面,抓取完成之后停止monitor
    web_spider.set_start_url("http://zhushou.360.cn/", ("360app",), priority=0, deep=0, critical=False)
    web_spider.start_work_and_wait_done(fetcher_num=10, parser_num=parser_num, is_over=True)
    return


if __name__ == "__main__":
    # 测试多线程抓取
    test_spider(spider_type="thread")

    # 测试多线程/多进程混合抓取
    test_spider(spider_type="process")

    exit()
