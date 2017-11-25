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

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        BaseThread.__init__(self, name, worker, pool)
        self._proxies = None        # proxies for fetching, if None, getting from proxies_queue
        return

    def working(self):
        """
        procedure of fetching, auto running, and return False if you need stop thread
        """
        # ----1----
        priority, url, keys, deep, repeat = self._pool.get_a_task(TPEnum.URL_FETCH)

        # ----2----
        fetch_result, content = self._worker.working(priority, url, keys, deep, repeat)

        # ----3----
        if fetch_result == 1:
            self._pool.update_number_dict(TPEnum.URL_FETCH_SUCC, +1)
            self._pool.add_a_task(TPEnum.HTM_PARSE, (priority, url, keys, deep, content))
        elif fetch_result == 0:
            self._pool.add_a_task(TPEnum.URL_FETCH, (priority+1, url, keys, deep, repeat+1))
        else:
            self._pool.update_number_dict(TPEnum.URL_FETCH_FAIL, +1)

        # ----4----
        self._pool.finish_a_task(TPEnum.URL_FETCH)

        # ----5----
        while (self._pool.get_number_dict(TPEnum.HTM_NOT_PARSE) > 500) or (self._pool.get_number_dict(TPEnum.ITEM_NOT_SAVE) > 500):
            logging.debug("%s[%s] sleep 5 seconds because of too many 'HTM_NOT_PARSE' or 'ITEM_NOT_SAVE'...", self.__class__.__name__, self.getName())
            time.sleep(5)
        return False if fetch_result == -2 else True
