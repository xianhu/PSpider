# _*_ coding: utf-8 _*_

"""
inst_parse.py by xianhu
"""

import re
import logging
import datetime
from ..utilities import get_url_legal


class Parser(object):
    """
    class of Parser, must include function working()
    """

    def __init__(self, max_deep=0):
        """
        constructor
        """
        self._max_deep = max_deep       # default: 0, if -1, spider will not stop until all urls are fetched
        return

    def working(self, priority: int, url: str, keys: object, deep: int, content: object) -> (int, list, list):
        """
        working function, must "try, except" and don't change parameters and return
        :return (parse_result, url_list, save_list): parse_result can be -1(parse failed), 1(parse success)
        :return (parse_result, url_list, save_list): url_list is [(url, keys, priority), ...], save_list is [item, ...]
        """
        logging.debug("%s start: priority=%s, keys=%s, deep=%s, url=%s", self.__class__.__name__, priority, keys, deep, url)

        try:
            parse_result, url_list, save_list = self.htm_parse(priority, url, keys, deep, content)
        except Exception as excep:
            parse_result, url_list, save_list = -1, [], []
            logging.error("%s error: %s, priority=%s, keys=%s, deep=%s, url=%s", self.__class__.__name__, excep, priority, keys, deep, url)

        logging.debug("%s end: parse_result=%s, len(url_list)=%s, len(save_list)=%s, url=%s", self.__class__.__name__, parse_result, len(url_list), len(save_list), url)
        return parse_result, url_list, save_list

    def htm_parse(self, priority: int, url: str, keys: object, deep: int, content: object) -> (int, list, list):
        """
        parse the content of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        # parse content(cur_code, cur_url, cur_html)
        *_, cur_html = content

        # get url_list
        url_list = []
        if (self._max_deep < 0) or (deep < self._max_deep):
            a_list = re.findall(r"<a[\w\W]+?href=\"(?P<url>[\w\W]{5,}?)\"[\w\W]*?>[\w\W]+?</a>", cur_html, flags=re.IGNORECASE)
            url_list = [(_url, keys, priority+1) for _url in [get_url_legal(href, url) for href in a_list]]
        else:
            logging.debug("%s stop parse urls: priority=%s, keys=%s, deep=%s, url=%s", self.__class__.__name__, priority, keys, deep, url)

        # get save_list
        title = re.search(r"<title>(?P<title>[\w\W]+?)</title>", cur_html, flags=re.IGNORECASE)
        save_list = [(title.group("title"), datetime.datetime.now()), ] if title else []

        # return parse_result, url_list, save_list
        return 1, url_list, save_list
