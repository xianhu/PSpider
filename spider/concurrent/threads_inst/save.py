# _*_ coding: utf-8 _*_

"""
save.py by xianhu
"""

import logging
from .base import TPEnum, BaseThread
from ...utilities import CONFIG_ERROR_MESSAGE, get_dict_buildin


class SaveThread(BaseThread):
    """
    class of SaveThread, as the subclass of BaseThread
    """

    def working(self):
        """
        procedure of saving, auto running, and return True
        """
        # ----1----
        priority, url, keys, deep, item = self._pool.get_a_task(TPEnum.ITEM_SAVE)

        # ----2----
        save_state, save_result = self._worker.working(priority, url, keys, deep, item)

        # ----3----
        self._pool.accept_state_from_task(TPEnum.ITEM_SAVE, save_state, (priority, url, keys, deep, item))

        # ----4----
        if save_state > 0:
            self._pool.update_number_dict(TPEnum.ITEM_SAVE_SUCC, +1)
        else:
            self._pool.update_number_dict(TPEnum.ITEM_SAVE_FAIL, +1)
            logging.error("%s error: %s, %s", save_result[0], save_result[1], CONFIG_ERROR_MESSAGE % (priority, get_dict_buildin(keys), deep, url))

        # ----5----
        self._pool.finish_a_task(TPEnum.ITEM_SAVE)

        # ----6----
        return True
