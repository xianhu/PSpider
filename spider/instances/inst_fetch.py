# _*_ coding: utf-8 _*_

"""
inst_fetch.py by xianhu
"""

import time
import random
import logging
import requests
from ..utilities import make_random_useragent


class Fetcher(object):
    """
    class of Fetcher, must include function working()
    """

    def __init__(self, max_repeat=3, sleep_time=0):
        """
        constructor
        """
        self._max_repeat = max_repeat       # default: 3, maximum repeat fetching time for a url
        self._sleep_time = sleep_time       # default: 0, sleeping time after a fetching for a url
        return

    def working(self, url: str, keys: object, repeat: int) -> (int, object):
        """
        working function, must "try, expect" and don't change parameters and return
        :return (fetch_result, content): fetch_result can be -1(fetch failed), 0(need repeat), 1(fetch success), content can be anything
        """
        logging.debug("%s start: keys=%s, repeat=%s, url=%s", self.__class__.__name__, keys, repeat, url)

        time.sleep(random.randint(0, self._sleep_time))
        try:
            fetch_result, content = self.url_fetch(url, keys, repeat)
        except Exception as excep:
            if repeat >= self._max_repeat:
                fetch_result, content = -1, None
                logging.error("%s error: %s, keys=%s, repeat=%s, url=%s", self.__class__.__name__, excep, keys, repeat, url)
            else:
                fetch_result, content = 0, None
                logging.debug("%s repeat: %s, keys=%s, repeat=%s, url=%s", self.__class__.__name__, excep, keys, repeat, url)

        logging.debug("%s end: fetch_result=%s, url=%s", self.__class__.__name__, fetch_result, url)
        return fetch_result, content

    def url_fetch(self, url: str, keys: object, repeat: int) -> (int, object):
        """
        fetch the content of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        # get response based on headers
        headers = {"User-Agent": make_random_useragent(), "Accept-Encoding": "gzip"}
        response = requests.get(url, params=None, data=None, headers=headers, cookies=None, timeout=(3.05, 10))
        if response.history:
            logging.debug("%s redirect: keys=%s, repeat=%s, url=%s", self.__class__.__name__, keys, repeat, url)

        # get content(cur_code, cur_url, cur_html)
        content = (response.status_code, response.url, response.text)

        # return fetch_result, content
        return 1, content
