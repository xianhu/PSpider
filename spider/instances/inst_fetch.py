# _*_ coding: utf-8 _*_

"""
inst_fetch.py by xianhu
"""

import time
import random
import logging
import requests
from ..utilities import CONFIG_FETCH_MESSAGE, get_dict_buildin


class Fetcher(object):
    """
    class of Fetcher, must include function working()
    """

    def __init__(self, max_repeat=3, sleep_time=0):
        """
        constructor
        :param max_repeat: default 3, maximum repeat count of a fetching
        :param sleep_time: default 0, sleeping time after a fetching
        """
        self._max_repeat = max_repeat
        self._sleep_time = sleep_time
        return

    def working(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None) -> (int, object, bool):
        """
        working function, must "try, except" and don't change the parameters and return
        :return fetch_state: can be -1(fetch failed), 0(need repeat), 1(fetch success)
        :return fetch_result: can be any object, for example string, list, None, etc
        :return proxies_state: can be False(unavaiable), True(avaiable)
        """
        logging.debug("%s start: %s", self.__class__.__name__, CONFIG_FETCH_MESSAGE % (priority, keys, deep, repeat, url))

        time.sleep(random.randint(0, self._sleep_time))
        try:
            fetch_state, fetch_result, proxies_state = self.url_fetch(priority, url, keys, deep, repeat, proxies=proxies)
        except Exception as excep:
            if repeat >= self._max_repeat:
                fetch_state, fetch_result, proxies_state = -1, None, False
                logging.error("%s error: %s, %s", self.__class__.__name__, excep, CONFIG_FETCH_MESSAGE % (priority, get_dict_buildin(keys), deep, repeat, url))
            else:
                fetch_state, fetch_result, proxies_state = 0, None, False
                logging.debug("%s repeat: %s, %s", self.__class__.__name__, excep, CONFIG_FETCH_MESSAGE % (priority, keys, deep, repeat, url))

        logging.debug("%s end: fetch_state=%s, proxies_state=%s, url=%s", self.__class__.__name__, fetch_state, proxies_state, url)
        return fetch_state, fetch_result, proxies_state

    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None) -> (int, object, bool):
        """
        fetch the content of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        response = requests.get(url, params=None, headers={}, data=None, proxies=proxies, timeout=(3.05, 10))
        if response.history:
            logging.debug("%s redirect: %s", self.__class__.__name__, CONFIG_FETCH_MESSAGE % (priority, keys, deep, repeat, url))

        result = (response.status_code, response.url, response.text)
        return 1, result, True
