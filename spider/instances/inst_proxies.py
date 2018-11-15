# _*_ coding: utf-8 _*_

"""
inst_proxies.py by xianhu
"""

import time
import logging


class Proxieser(object):
    """
    class of Proxieser, must include function working()
    """

    def __init__(self, sleep_time=10):
        """
        constructor
        :param sleep_time: default 10, sleeping time after a fetching
        """
        self._sleep_time = sleep_time
        return

    def working(self) -> (int, list):
        """
        working function, must "try, except" and don't change the parameters and return
        :return proxies_state: can be -1(get failed), 1(get success)
        :return proxies_list: [{"http": "http://auth@ip:port", "https": "https://auth@ip:port"}, ...]
        """
        logging.debug("%s start", self.__class__.__name__)

        time.sleep(self._sleep_time)
        try:
            proxies_state, proxies_list = self.proxies_get()
        except Exception as excep:
            proxies_state, proxies_list = -1, []
            logging.error("%s error: %s", self.__class__.__name__, excep)

        logging.debug("%s end: proxies_state=%s, len(proxies_list)=%s", self.__class__.__name__, proxies_state, len(proxies_list))
        return proxies_state, proxies_list

    def proxies_get(self) -> (int, list):
        """
        get proxies from web or database, you can rewrite this function, parameters and return refer to self.working()
        """
        raise NotImplementedError
