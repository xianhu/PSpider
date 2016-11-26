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
        :return (code, url_list, save_list): code can be -1(parse failed), 0(need repeat), 1(parse success)
        :return (code, url_list, save_list): url_list is [(url, keys, critical, priority), ...], save_list is [item, ...]
        """
        logging.debug("%s start: %s", self.__class__.__name__, self.log_str_format % (priority, keys, deep, critical, parse_repeat, url))

        try:
            code, url_list, save_list = self.htm_parse(priority, url, keys, deep, critical, parse_repeat, content)
        except Exception as excep:
            if parse_repeat >= self.max_repeat:
                code, url_list, save_list = -1, [], []
                logging.error("%s error: %s, %s", self.__class__.__name__, excep, self.log_str_format % (priority, keys, deep, critical, parse_repeat, url))
            else:
                code, url_list, save_list = 0, [], []
                logging.debug("%s repeat: %s, %s", self.__class__.__name__, excep, self.log_str_format % (priority, keys, deep, critical, parse_repeat, url))

        logging.debug("%s end: code=%s, len(url_list)=%s, len(save_list)=%s, url=%s", self.__class__.__name__, code, len(url_list), len(save_list), url)
        return code, url_list, save_list

    @return_check(int, (tuple, list), (tuple, list))
    def htm_parse(self, priority, url, keys, deep, critical, parse_repeat, content):
        """
        parse the content of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        # parse content(cur_code, cur_url, cur_html)
        *_, cur_html = content

        # get url_list
        url_list = []
        if (self.max_deep < 0) or (deep < self.max_deep):
            a_list = re.findall(r"<a[\w\W]+?href=\"(?P<url>[\w\W]{5,}?)\"[\w\W]*?>[\w\W]+?</a>", cur_html, flags=re.IGNORECASE)
            url_list = [(_url, keys, critical, priority+1) for _url in [get_url_legal(href, url) for href in a_list]]
        else:
            logging.debug("%s stop parse urls: %s", self.__class__.__name__, self.log_str_format % (priority, keys, deep, critical, parse_repeat, url))

        # get save_list
        title = re.search(r"<title>(?P<title>[\w\W]+?)</title>", cur_html, flags=re.IGNORECASE)
        save_list = [(url, title.group("title"), datetime.datetime.now()), ] if title else []

        # test parsing error
        code = (1/0) if random.randint(0, 5) == 3 else 1

        # return code, url_list, save_list
        return code, url_list, save_list
