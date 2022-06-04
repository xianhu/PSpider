# _*_ coding: utf-8 _*_

"""
inst_fetch.py by xianhu
"""

import time
from ..utilities.util_result import ResultF


class Fetcher(object):
    """
    class of Fetcher, must include function working()
    """

    def __init__(self, sleep_time=0, max_repeat=3):
        """
        constructor
        :param sleep_time: default 0, sleeping time before fetching
        :param max_repeat: default 3, maximum repeat count of fetching
        """
        self._sleep_time = sleep_time
        self._max_repeat = max_repeat
        return

    def working(self, task, proxies=None) -> ResultF:
        """
        working function, must "try-except" and don't change the parameters and returns
        :return fetch_state: can be -1(fetch failed), 0(need repeat), 1(fetch success)
        :return content: which waits to be parsed, can be any object, or exception[class_name, excep]
        :return proxies_state: can be -1(unavaiable), 0(return to queue), 1(avaiable)
        """
        time.sleep(self._sleep_time)

        try:
            # fetch_state, content, proxies_state = self.url_fetch(task, proxies=proxies)
            result = self.url_fetch(task, proxies=proxies)
        except Exception as excep:
            result = ResultF(state_code=(-1 if repeat >= self._max_repeat else 0), )
            fetch_state, content, proxies_state = (-1 if repeat >= self._max_repeat else 0), [self.__class__.__name__, excep], -1

        return result

    def url_fetch(self, task, proxies=None) -> ResultF:
        """
        fetch the content of an url. You must overwrite this function
        """
        raise NotImplementedError
