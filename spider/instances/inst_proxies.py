# _*_ coding: utf-8 _*_

"""
inst_proxies.py by xianhu
"""

import time
from ..utilities import ResultProxies


class Proxieser(object):
    """
    class of Proxieser, must include function working()
    """

    def __init__(self, sleep_time=10):
        """
        constructor
        :param sleep_time: default 10, sleeping time before fetching
        """
        self._sleep_time = sleep_time
        return

    def working(self) -> ResultProxies:
        """
        working function, must "try-except"
        """
        time.sleep(self._sleep_time)

        try:
            result_proxies = self.proxies_get()
        except Exception as excep:
            kwargs = dict(excep_class=self.__class__.__name__, excep_string=str(excep))
            result_proxies = ResultProxies(state_code=-1, proxies_list=None, **kwargs)

        return result_proxies

    def proxies_get(self) -> ResultProxies:
        """
        get proxies from web or database. Parameters and returns refer to self.working()
        """
        raise NotImplementedError
