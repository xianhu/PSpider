# _*_ coding: utf-8 _*_

"""
inst_fetch.py by xianhu
"""

import time
from ..utilities import ResultFetch


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

    def working(self, task, proxies=None) -> ResultFetch:
        """
        working function, must "try-except" and don't change the parameters and returns
        """
        time.sleep(self._sleep_time)

        try:
            result = self.url_fetch(task, proxies=proxies)
        except Exception as excep:
            result = ResultFetch(
                state_code=(-1 if task.repeat >= self._max_repeat else 0),
                excep_class=self.__class__.__name__,
                excep_string=str(excep),
            )

        return result

    def url_fetch(self, task, proxies=None) -> ResultFetch:
        """
        fetch the content of an url. You must overwrite this function
        """
        raise NotImplementedError
