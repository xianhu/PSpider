# _*_ coding: utf-8 _*_

"""
inst_proxies.py by xianhu
"""

import time


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
        working function, must "try, except" and don't change the parameters and returns
        :return proxies_state: can be -1(get failed), 1(get success)
        :return proxies_list: [{"http(s)": "http(s)://auth@ip:port", ...], or exception information[class_name, excep]
        """
        time.sleep(self._sleep_time)

        try:
            proxies_state, proxies_list = self.proxies_get()
        except Exception as excep:
            proxies_state, proxies_list = -1, [self.__class__.__name__, str(excep)]

        return proxies_state, proxies_list

    def proxies_get(self) -> (int, list):
        """
        get proxies from web or database, you must overwrite this function, parameters and returns refer to self.working()
        """
        raise NotImplementedError
