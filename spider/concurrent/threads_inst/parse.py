# _*_ coding: utf-8 _*_

"""
parse.py by xianhu
"""

import logging
import multiprocessing
from .base import TPEnum, BaseThread
from ...utilities import CONFIG_ERROR_MESSAGE, check_url_legal, get_dict_buildin


class ParseThread(BaseThread):
    """
    class of ParseThread, as the subclass of BaseThread
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        BaseThread.__init__(self, name, worker, pool)
        self._pool_multiprocssing = multiprocessing.Pool()
        return

    def working(self):
        """
        procedure of parsing, auto running, and return True
        """
        # ----1----
        task_list = [self._pool.get_a_task(TPEnum.HTM_PARSE) for _ in range(max(1, self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT)))]

        # ----2----
        result_list = [self._pool_multiprocssing.apply_async(self._worker.working, args=task) for task in task_list]

        for index in range(len(task_list)):
            priority, url, keys, deep, content = task_list[index]
            parse_state, url_list, item = result_list[index].get(timeout=None)

            # ----3----
            self._pool.accept_state_from_task(TPEnum.HTM_PARSE, parse_state, (priority, url, keys, deep, content))

            # ----4----
            if parse_state > 0:
                self._pool.update_number_dict(TPEnum.HTM_PARSE_SUCC, +1)
                for _url, _keys, _priority in filter(lambda x: check_url_legal(x[0]), url_list):
                    self._pool.add_a_task(TPEnum.URL_FETCH, (_priority, _url, _keys, deep+1, 0))
                if item is not None:
                    self._pool.add_a_task(TPEnum.ITEM_SAVE, (priority, url, keys, deep, item))
            else:
                self._pool.update_number_dict(TPEnum.HTM_PARSE_FAIL, +1)
                logging.error("%s error: %s, %s", url_list[0], url_list[1], CONFIG_ERROR_MESSAGE % (priority, get_dict_buildin(keys), deep, url))

            # ----5----
            self._pool.finish_a_task(TPEnum.HTM_PARSE)

        # ----6----
        return True
