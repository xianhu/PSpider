# _*_ coding: utf-8 _*_

"""
inst_parse.py by xianhu
"""

import re
import random
import logging
import datetime
from ..utilities import get_url_legal, params_chack, return_check


class Parser(object):
    """
    class of Parser, must include function working() and htm_parse()
    """

    def __init__(self, max_deep=0, max_repeat=0):
        """
        constructor
        """
        self.max_deep = max_deep        # default: 0, if -1, spider will not stop until all urls are fetched
        self.max_repeat = max_repeat    # default: 0, maximum repeat time for parsing content

        self.log_str_format = "priority=%s, keys=%s, deep=%s, critical=%s, parse_repeat=%s, url=%s"
        return

    @params_chack(object, int, str, object, int, bool, int, object)
    def working(self, priority, url, keys, deep, critical, parse_repeat, content):
        """
        working function, must "try, except" and call self.htm_parse(), don't change parameters and return
        :param priority: the priority of this url, which can be used in this function
        :param url: the url, whose content needs to be parsed
        :param keys: some information of this url, which can be used in this function
        :param deep: the deep of this url, which can be used in this function
        :param critical: the critical flag of this url, which can be used in this function
        :param parse_repeat: the parse repeat time of this url, if parse_repeat >= self.max_repeat, return code = -1
        :param content: the content of this url, which needs to be parsed, content is transfered from Fetcher
        :return (code, url_list, save_list): code can be -1(parse failed), 0(need repeat), 1(parse success)
        :return (code, url_list, save_list): url_list is [(url, keys, critical, priority), ...], save_list is [item, ...]
        """
        logging.debug("Parser start: %s", self.log_str_format % (priority, keys, deep, critical, parse_repeat, url))

        try:
            code, url_list, save_list = self.htm_parse(priority, url, keys, deep, critical, parse_repeat, content)
        except Exception as excep:
            if parse_repeat >= self.max_repeat:
                code, url_list, save_list = -1, [], []
                logging.error("Parser error: %s, %s", excep, self.log_str_format % (priority, keys, deep, critical, parse_repeat, url))
            else:
                code, url_list, save_list = 0, [], []
                logging.debug("Parser repeat: %s, %s", excep, self.log_str_format % (priority, keys, deep, critical, parse_repeat, url))

        logging.debug("Parser end: code=%s, len(url_list)=%s, len(save_list)=%s, url=%s", code, len(url_list), len(save_list), url)
        return code, url_list, save_list

    @return_check(int, (tuple, list), (tuple, list))
    def htm_parse(self, priority, url, keys, deep, critical, parse_repeat, content):
        """
        parse the content of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        # parse content(cur_code, cur_url, cur_html)
        cur_code, cur_url, cur_html = content

        # get url_list and save_list
        url_list = []
        if (self.max_deep < 0) or (deep < self.max_deep):
            a_list = re.findall(r"<a[\w\W]+?href=\"(?P<url>[\w\W]{5,}?)\"[\w\W]*?>[\w\W]+?</a>", cur_html, flags=re.IGNORECASE)
            url_list = [(_url, keys, critical, priority+1) for _url in [get_url_legal(href, url) for href in a_list]]
        title = re.search(r"<title>(?P<title>[\w\W]+?)</title>", cur_html, flags=re.IGNORECASE)
        save_list = [(url, title.group("title"), datetime.datetime.now()), ] if title else []

        # test cpu task
        sum([(i*j)/1000 for i in range(1000) for j in range(1000)])

        # test parsing error
        code = (1/0) if random.randint(0, 5) == 3 else 1

        # return code, url_list, save_list
        return code, url_list, save_list
