# _*_ coding: utf-8 _*_

"""
inst_fetch.py by xianhu
"""

import time
import random
import logging
import requests
from ..utilities import CONFIG_ERROR_MESSAGE, make_random_useragent


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

    def working(self, priority: int, url: str, keys: object, deep: int, repeat: int) -> (int, object):
        """
        working function, must "try, expect" and don't change the parameters and return
        :return (fetch_result, content): fetch_result can be -2(fetch failed, need stop thread), -1(fetch failed), 0(need repeat), 1(fetch success)
        :return (fetch_result, content): content can be any object, for example: string, list, etc
        """
        logging.debug("%s start: priority=%s, keys=%s, deep=%s, repeat=%s, url=%s", self.__class__.__name__, priority, keys, deep, repeat, url)

        time.sleep(random.randint(0, self._sleep_time))
        try:
            fetch_result, content = self.url_fetch(priority, url, keys, deep, repeat)
        except Exception as excep:
            if repeat >= self._max_repeat:
                fetch_result, content = -1, None
                logging.error("%s error: %s, %s", self.__class__.__name__, excep, CONFIG_ERROR_MESSAGE % (priority, keys, deep, url))
            else:
                fetch_result, content = 0, None
                logging.debug("%s repeat: %s, priority=%s, keys=%s, deep=%s, repeat=%s, url=%s", self.__class__.__name__, excep, priority, keys, deep, repeat, url)

        logging.debug("%s end: fetch_result=%s, url=%s", self.__class__.__name__, fetch_result, url)
        return fetch_result, content

    def url_fetch(self, priority: int, url: str, keys: object, deep: int, repeat: int) -> (int, object):
        """
        fetch the content of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        response = requests.get(url, headers={"User-Agent": make_random_useragent(), "Accept-Encoding": "gzip"}, timeout=(3.05, 10))
        if response.history:
            logging.debug("%s redirect: priority=%s, keys=%s, deep=%s, repeat=%s, url=%s", self.__class__.__name__, priority, keys, deep, repeat, url)

        content = (response.status_code, response.url, response.text)
        return 1, content
