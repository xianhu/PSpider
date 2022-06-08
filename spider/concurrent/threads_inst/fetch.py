# _*_ coding: utf-8 _*_

"""
fetch.py by xianhu
"""

import logging

from .base import TPEnum, BaseThread
from ...utilities import TaskFetch


class FetchThread(BaseThread):
    """
    class of FetchThread, as the subclass of BaseThread
    """

    def __init__(self, name, worker, pool):
        """
        constructor, add proxies to this thread
        """
        BaseThread.__init__(self, name, worker, pool)
        self._proxies = None
        return

    def working(self):
        """
        procedure of fetching, auto running and return True
        """
        # ----*----
        if self._pool.get_proxies_flag() and (not self._proxies):
            self._proxies = self._pool.get_a_task(TPEnum.PROXIES)

        # ----1----
        task_fetch = self._pool.get_a_task(TPEnum.URL_FETCH)

        # ----2----
        result_fetch = self._worker.working(task_fetch, proxies=self._proxies)

        # ----3----
        if result_fetch.state_code > 0:
            self._pool.update_number_dict(TPEnum.URL_FETCH_SUCC, +1)
            self._pool.add_a_task(TPEnum.HTM_PARSE, result_fetch.task_parse)
        elif result_fetch.state_code == 0:
            self._pool.add_a_task(TPEnum.URL_FETCH, TaskFetch.from_task_fetch(task_fetch))
            logging.warning("%s repeat: %s, %s", result_fetch.excep_class, result_fetch.excep_string, str(task_fetch))
        else:
            self._pool.update_number_dict(TPEnum.URL_FETCH_FAIL, +1)
            logging.warning("%s repeat: %s, %s", result_fetch.excep_class, result_fetch.excep_string, str(task_fetch))

        # ----*----
        if self._pool.get_proxies_flag() and self._proxies and (result_fetch.state_proxies <= 0):
            if result_fetch.state_proxies == 0:
                self._pool.add_a_task(TPEnum.PROXIES, self._proxies)
            else:
                self._pool.update_number_dict(TPEnum.PROXIES_FAIL, +1)
            self._pool.finish_a_task(TPEnum.PROXIES)
            self._proxies = None

        # ----4----
        self._pool.finish_a_task(TPEnum.URL_FETCH)

        # ----5----
        return True
