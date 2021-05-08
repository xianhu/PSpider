# _*_ coding: utf-8 _*_

"""
parse.py by xianhu
"""

import logging
from .base import TPEnum, BaseThread
from ...utilities import CONFIG_ERROR_MESSAGE, get_dict_buildin, check_url_legal


class ParseThread(BaseThread):
    """
    class of ParseThread, as the subclass of BaseThread
    """

    def working(self):
        """
        procedure of parsing, auto running and return True
        """
        # ----1----
        priority, url, keys, deep, content = self._pool.get_a_task(TPEnum.HTM_PARSE)

        # ----2----
        parse_state, url_list, item = self._worker.working(priority, url, keys, deep, content)

        # ----3----
        if parse_state > 0:
            self._pool.update_number_dict(TPEnum.HTM_PARSE_SUCC, +1)
            for _url, _keys, _priority in filter(lambda x: check_url_legal(x[0]), url_list):
                self._pool.add_a_task(TPEnum.URL_FETCH, (_priority, _url, _keys, deep + 1, 0))
            if item is not None:
                self._pool.add_a_task(TPEnum.ITEM_SAVE, (priority, url, keys, deep, item))
        else:
            self._pool.update_number_dict(TPEnum.HTM_PARSE_FAIL, +1)
            logging.error("%s error: %s, %s", url_list[0], url_list[1], CONFIG_ERROR_MESSAGE % (priority, get_dict_buildin(keys), deep, url))

        # ----4----
        self._pool.finish_a_task(TPEnum.HTM_PARSE)

        # ----5----
        return True
