# _*_ coding: utf-8 _*_

"""
inst_parse.py by xianhu
"""

import random
import logging
import datetime
import bs4
from ..utilities import get_string_strip, get_url_legal, params_chack


class Item(object):
    """
    class of Item, as an example of item
    """

    def __init__(self, url, title, getdate):
        """
        constructor
        """
        self.url = url
        self.title = title
        self.getdate = getdate
        return

    def get_list(self):
        """
        get a list based on variables of this class
        """
        return [self.url, self.title, self.getdate]


class Parser(object):
    """
    class of Parser, must include function working() and htm_parse()
    """

    def __init__(self, max_deep=0, max_repeat=3):
        """
        constructor
        """
        self.max_deep = max_deep        # default: 0, if -1, spider will not stop until all urls are fetched
        self.max_repeat = max_repeat    # default: 3, maximum repeat time for parsing content
        return

    @params_chack(object, int, str, object, int, bool, int, (list, tuple))
    def working(self, priority, url, keys, deep, critical, parse_repeat, content):
        """
        working function, must "try, except" and call self.htm_parse(), don't change parameters and returns
        :return (code, url_list, save_list): code can be -1(failed), 0(repeat), 1(success); [(url, keys, critical, priority), ...], [item, ...]
        """
        logging.debug("Parser start: priority=%s, keys=%s, deep=%s, critical=%s, parse_repeat=%s, url=%s",
                      priority, keys, deep, critical, parse_repeat, url)

        try:
            code, url_list, save_list = self.htm_parse(priority, url, keys, deep, critical, parse_repeat, content)
        except Exception as excep:
            if parse_repeat >= self.max_repeat:
                code, url_list, save_list = -1, [], []
                logging.error("Parser error: %s, priority=%s, keys=%s, deep=%s, critical=%s, parse_repeat=%s, url=%s",
                              excep, priority, keys, deep, critical, parse_repeat, url)
            else:
                code, url_list, save_list = 0, [], []
                logging.debug("Parser repeat: %s, priority=%s, keys=%s, deep=%s, critical=%s, parse_repeat=%s, url=%s",
                              excep, priority, keys, deep, critical, parse_repeat, url)

        logging.debug("Parser end: code=%s, len(url_list)=%s, len(save_list)=%s, url=%s", code, len(url_list), len(save_list), url)
        return code, url_list, save_list

    def htm_parse(self, priority, url, keys, deep, critical, parse_repeat, content):
        """
        parse the content of a url, you can rewrite this function
        :return (code, url_list, save_list): code can be -1(failed), 0(repeat), 1(success); [(url, keys, critical, priority), ...], [item, ...]
        """
        # parse content (cur_code, cur_url, cur_info, cur_html)
        *_, cur_html = content
        soup = bs4.BeautifulSoup(cur_html, "html.parser")

        # get url_list and save_list
        url_list = []
        if (self.max_deep < 0) or (deep < self.max_deep):
            url_list = [(_url, keys, critical, priority+1) for _url in [get_url_legal(a.get("href"), url) for a in soup.find_all("a")]]
        save_list = [Item(url, get_string_strip(soup.title.string), datetime.datetime.now()), ]

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
