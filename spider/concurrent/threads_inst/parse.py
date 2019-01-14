# _*_ coding: utf-8 _*_

"""
parse.py by xianhu
"""

import logging
import multiprocessing
from .base import TPEnum, BaseThread
from ...utilities import CONFIG_PARSE_MESSAGE, check_url_legal, get_dict_buildin


class ParseThread(BaseThread):
    """
    class of ParseThread, as the subclass of BaseThread
    """

    def working(self):
        """
        procedure of parsing, auto running, and return True
        """
        if self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT) <= self._pool.get_fetcher_number() / 2:
            # ----1----
            task_list = [self._pool.get_a_task(TPEnum.HTM_PARSE) for _ in range(1)]
            # ----2----
            pool = None
            result_list = [self._worker.working(task[0], task[2], task[3], task[4], task[5]) for task in task_list]
        else:
            # ----1----
            task_list = [self._pool.get_a_task(TPEnum.HTM_PARSE) for _ in range(self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT))]
            # ----2----
            pool = multiprocessing.Pool()
            result_list = [pool.apply_async(self._worker.working, args=(task[0], task[2], task[3], task[4], task[5])) for task in task_list]
            pool.close()

        for index in range(len(task_list)):
            priority, counter, url, keys, deep, content = task_list[index]
            parse_state, url_list, save_list = result_list[index] if (pool is None) else result_list[index].get(timeout=None)

            # ----3----
            if parse_state > 0:
                self._pool.update_number_dict(TPEnum.HTM_PARSE_SUCC, +1)
                for _url, _keys, _priority in filter(lambda x: check_url_legal(x[0]), url_list):
                    self._pool.add_a_task(TPEnum.URL_FETCH, (_priority, self._pool.get_number_dict(TPEnum.URL_COUNTER), _url, _keys, deep+1, 0))
                for item in save_list:
                    self._pool.add_a_task(TPEnum.ITEM_SAVE, (url, keys, item))
            else:
                self._pool.update_number_dict(TPEnum.HTM_PARSE_FAIL, +1)
                logging.error("%s error: %s, %s", url_list[0], url_list[1], CONFIG_PARSE_MESSAGE % (priority, get_dict_buildin(keys), deep, url))

            # ----4----
            self._pool.finish_a_task(TPEnum.HTM_PARSE)

        # ----5----
        return True
