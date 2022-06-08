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
        task_parse: TaskParse = self._pool.get_a_task(TPEnum.HTM_PARSE)

        # ----2----
        result_parse: ResultParse = self._worker.working(task_parse)

        # ----3----
        if result_parse.state_code > 0:
            self._pool.update_number_dict(TPEnum.HTM_PARSE_SUCC, +1)
            for task_fetch in result_parse.task_fetch_list:
                self._pool.add_a_task(TPEnum.URL_FETCH, task_fetch)
            if result_parse.task_save is not None:
                self._pool.add_a_task(TPEnum.ITEM_SAVE, result_parse.task_save)
        else:
            self._pool.update_number_dict(TPEnum.HTM_PARSE_FAIL, +1)
            logging.error("%s error: %s, %s", result_parse.excep_class, result_parse.excep_string, str(task_parse))

        # ----4----
        self._pool.finish_a_task(TPEnum.HTM_PARSE)

        # ----5----
        return True
