# _*_ coding: utf-8 _*_

"""
save.py by xianhu
"""

import logging

from .base import TPEnum, BaseThread
from ...utilities.util_funcs import get_dict_buildin
from ...utilities.util_config import CONFIG_TM_ERROR_MESSAGE


class SaveThread(BaseThread):
    """
    class of SaveThread, as the subclass of BaseThread
    """

    def working(self):
        """
        procedure of saving, auto running and return True
        """
        # ----1----
        priority, url, keys, deep, item = self._pool.get_a_task(TPEnum.ITEM_SAVE)

        # ----2----
        save_state, save_result = self._worker.working(priority, url, keys, deep, item)

        # ----3----
        if save_state > 0:
            self._pool.update_number_dict(TPEnum.ITEM_SAVE_SUCC, +1)
        else:
            self._pool.update_number_dict(TPEnum.ITEM_SAVE_FAIL, +1)
            logging.error("%s error: %s, %s", save_result[0], save_result[1], CONFIG_TM_ERROR_MESSAGE % (priority, get_dict_buildin(keys), deep, url))

        # ----4----
        self._pool.finish_a_task(TPEnum.ITEM_SAVE)

        # ----5----
        return True
