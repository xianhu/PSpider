# _*_ coding: utf-8 _*_

"""
save.py by xianhu
"""

import logging
from .base import TPEnum, BaseThread
from ...utilities import get_dict_buildin


class SaveThread(BaseThread):
    """
    class of SaveThread, as the subclass of BaseThread
    """

    def working(self):
        """
        procedure of saving, auto running, and return True
        """
        # ----1----
        url, keys, item = self._pool.get_a_task(TPEnum.ITEM_SAVE)

        # ----2----
        save_state, save_result = self._worker.working(url, keys, item)

        # ----3----
        if save_state > 0:
            self._pool.update_number_dict(TPEnum.ITEM_SAVE_SUCC, +1)
        else:
            self._pool.update_number_dict(TPEnum.ITEM_SAVE_FAIL, +1)
            logging.error("%s error: %s, keys=%s, url=%s", save_result[0], save_result[1], get_dict_buildin(keys), url)

        # ----4----
        self._pool.finish_a_task(TPEnum.ITEM_SAVE)

        # ----5----
        return True
