# _*_ coding: utf-8 _*_

"""
parse.py by xianhu
"""

import logging

from .base import TPEnum, BaseThread
from ...utilities import TaskParse, ResultParse


class ParseThread(BaseThread):
    """
    class of ParseThread, as the subclass of BaseThread
    """

    def working(self):
        """
        procedure of parsing, auto running and return True
        """
        # ----1----
        task: TaskParse = self._pool.get_a_task(TPEnum.HTM_PARSE)

        # ----2----
        result: ResultParse = self._worker.working(task)

        # ----3----
        if result.state_code > 0:
            self._pool.update_number_dict(TPEnum.HTM_PARSE_SUCC, +1)
            for task_fetch in result.task_fetch_list:
                self._pool.add_a_task(TPEnum.URL_FETCH, task_fetch)
            if result.task_save is not None:
                self._pool.add_a_task(TPEnum.ITEM_SAVE, result.task_save)
        else:
            self._pool.update_number_dict(TPEnum.HTM_PARSE_FAIL, +1)
            logging.error("%s error: %s, %s", result.excep_class, result.excep_string, str(task))

        # ----4----
        self._pool.finish_a_task(TPEnum.HTM_PARSE)

        # ----5----
        return True
