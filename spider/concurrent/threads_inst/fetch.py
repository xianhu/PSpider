# _*_ coding: utf-8 _*_

"""
fetch.py by xianhu
"""

import logging
from .base import TPEnum, BaseThread
from ...utilities import CONFIG_ERROR_MESSAGE, get_dict_buildin


class FetchThread(BaseThread):
    """
    class of FetchThread, as the subclass of BaseThread
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        BaseThread.__init__(self, name, worker, pool)
        self._proxies = None
        return

    def working(self):
        """
        procedure of fetching, auto running, and return True
        """
        # ----0----
        if self._pool.get_proxies_flag() and (not self._proxies):
            self._proxies = self._pool.get_a_task(TPEnum.PROXIES)

        # ----1----
        priority, counter, url, keys, deep, repeat = self._pool.get_a_task(TPEnum.URL_FETCH)

        # ----2----
        fetch_state, content, proxies_state = self._worker.working(priority, url, keys, deep, repeat, proxies=self._proxies)

        # ----3----
        if fetch_state > 0:
            self._pool.update_number_dict(TPEnum.URL_FETCH_SUCC, +1)
            self._pool.add_a_task(TPEnum.HTM_PARSE, (priority, counter, url, keys, deep, content))
        elif fetch_state == 0:
            self._pool.add_a_task(TPEnum.URL_FETCH, (priority, counter, url, keys, deep, repeat+1))
        else:
            self._pool.update_number_dict(TPEnum.URL_FETCH_FAIL, +1)
            logging.error("%s error: %s, %s", content[0], content[1], CONFIG_ERROR_MESSAGE % (priority, get_dict_buildin(keys), deep, url))

        # ----*----
        if self._proxies and (proxies_state <= 0):
            if proxies_state == 0:
                self._pool.add_a_task(TPEnum.PROXIES, self._proxies)
            else:
                self._pool.update_number_dict(TPEnum.PROXIES_FAIL, +1)
            self._pool.finish_a_task(TPEnum.PROXIES)
            self._proxies = None

        # ----4----
        self._pool.finish_a_task(TPEnum.URL_FETCH)

        # ----5----
        return True
