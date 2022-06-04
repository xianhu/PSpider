# _*_ coding: utf-8 _*_

"""
fetch.py by xianhu
"""

import logging

from .base import TPEnum, BaseThread
from ...utilities.util_task import TaskF, TaskP


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
        task = self._pool.get_a_task(TPEnum.URL_FETCH)

        # ----2----
        result = self._worker.working(task, proxies=self._proxies)

        # ----3----
        if result.state_code > 0:
            self._pool.update_number_dict(TPEnum.URL_FETCH_SUCC, +1)
            self._pool.add_a_task(TPEnum.HTM_PARSE, TaskP(task.url, task.priority, task.keys, task.deep, result.html))
        elif result.state_code == 0:
            self._pool.add_a_task(TPEnum.URL_FETCH, TaskF(task.url, task.priority, task.keys, task.deep, task.repeat + 1))
            logging.warning("%s repeat: %s, %s", result.class_name, result.excep, task)
        else:
            self._pool.update_number_dict(TPEnum.URL_FETCH_FAIL, +1)
            logging.warning("%s repeat: %s, %s", result.class_name, result.excep, task)

        # ----*----
        if self._pool.get_proxies_flag() and self._proxies and (proxies_state <= 0):
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
