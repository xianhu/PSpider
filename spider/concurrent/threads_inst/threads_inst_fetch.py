# _*_ coding: utf-8 _*_

"""
threads_inst_fetch.py by xianhu
"""

import time
import logging
from .threads_inst_base import TPEnum, BaseThread


class FetchThread(BaseThread):
    """
    class of FetchThread, as the subclass of BaseThread
    """

    def __init__(self, name, worker, pool, max_count=500):
        """
        constructor
        """
        BaseThread.__init__(self, name, worker, pool)
        self._max_count = max_count
        self._proxies = None
        return

    def working(self):
        """
        procedure of fetching, auto running, and return True
        """
        # ----*----
        if self._pool.get_proxies_flag() and (not self._proxies):
            self._proxies = self._pool.get_a_task(TPEnum.PROXIES)

        # ----1----
        priority, counter, url, keys, deep, repeat = self._pool.get_a_task(TPEnum.URL_FETCH)

        # ----2----
        fetch_result, proxies_state, content = self._worker.working(priority, url, keys, deep, repeat, proxies=self._proxies)

        # ----3----
        if fetch_result > 0:
            self._pool.update_number_dict(TPEnum.URL_FETCH_SUCC, +1)
            if content is not None:
                self._pool.add_a_task(TPEnum.HTM_PARSE, (priority, counter, url, keys, deep, content))
        elif fetch_result == 0:
            self._pool.add_a_task(TPEnum.URL_FETCH, (priority, counter, url, keys, deep, repeat+1))
        else:
            self._pool.update_number_dict(TPEnum.URL_FETCH_FAIL, +1)

        # ----*----
        if self._proxies and (not proxies_state):
            self._pool.update_number_dict(TPEnum.PROXIES_FAIL, +1)
            self._pool.finish_a_task(TPEnum.PROXIES)
            self._proxies = None

        # ----4----
        self._pool.finish_a_task(TPEnum.URL_FETCH)

        # ----*----
        while (self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT) > self._max_count) or (self._pool.get_number_dict(TPEnum.ITEM_SAVE_NOT) > self._max_count):
            logging.debug("%s[%s] sleep 5 seconds because of too many 'HTM_PARSE_NOT' or 'ITEM_SAVE_NOT'...", self.__class__.__name__, self.getName())
            time.sleep(5)

        # ----5----
        return True
