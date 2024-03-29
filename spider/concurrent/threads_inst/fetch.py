# _*_ coding: utf-8 _*_

"""
fetch.py by xianhu
"""

import logging

from .base import TPEnum, BaseThread
from ...utilities import TaskFetch, ResultFetch


class FetchThread(BaseThread):
    """
    class of FetchThread, as the subclass of BaseThread
    """

    def __init__(self, name, worker, pool):
        """
        constructor, add proxies to this thread
        """
        super().__init__(name, worker, pool)
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
        task: TaskFetch = self._pool.get_a_task(TPEnum.URL_FETCH)

        # ----2----
        result: ResultFetch = self._worker.working(task, proxies=self._proxies)

        # ----3----
        if result.state_code > 0:
            self._pool.update_number_dict(TPEnum.URL_FETCH_SUCC, +1)
            self._pool.add_a_task(TPEnum.HTM_PARSE, result.task_parse)
        elif result.state_code == 0:
            self._pool.add_a_task(TPEnum.URL_FETCH, TaskFetch.from_task_fetch(task))
            logging.warning("%s repeat: %s, %s", result.excep_class, result.excep_string, str(task))
        else:
            self._pool.update_number_dict(TPEnum.URL_FETCH_FAIL, +1)
            logging.error("%s error: %s, %s", result.excep_class, result.excep_string, str(task))

        # ----4----
        self._pool.finish_a_task(TPEnum.URL_FETCH)

        # ----*----
        if self._pool.get_proxies_flag() and self._proxies and (result.state_proxies <= 0):
            if result.state_proxies == 0:
                self._pool.add_a_task(TPEnum.PROXIES, self._proxies)
            else:
                self._pool.update_number_dict(TPEnum.PROXIES_FAIL, +1)
            self._pool.finish_a_task(TPEnum.PROXIES)
            self._proxies = None

        # return
        return True
