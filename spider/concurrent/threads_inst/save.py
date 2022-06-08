# _*_ coding: utf-8 _*_

"""
save.py by xianhu
"""

import logging

from .base import TPEnum, BaseThread
from ...utilities import TaskSave, ResultSave


class SaveThread(BaseThread):
    """
    class of SaveThread, as the subclass of BaseThread
    """

    def working(self):
        """
        procedure of saving, auto running and return True
        """
        # ----1----
        task: TaskSave = self._pool.get_a_task(TPEnum.ITEM_SAVE)

        # ----2----
        result: ResultSave = self._worker.working(task)

        # ----3----
        if result.state_code > 0:
            self._pool.update_number_dict(TPEnum.ITEM_SAVE_SUCC, +1)
        else:
            self._pool.update_number_dict(TPEnum.ITEM_SAVE_FAIL, +1)
            logging.error("%s error: %s, %s", result.excep_class, result.excep_string, str(task))

        # ----4----
        self._pool.finish_a_task(TPEnum.ITEM_SAVE)

        # ----5----
        return True
