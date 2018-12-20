# _*_ coding: utf-8 _*_

"""
parse.py by xianhu
"""

import multiprocessing
from .base import TPEnum, BaseThread


class ParseThread(BaseThread):
    """
    class of ParseThread, as the subclass of BaseThread
    """

    def working(self):
        """
        procedure of parsing, auto running, and return True
        """
        if self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT) <= self._pool.get_fetcher_number():
            # ----1----
            priority, counter, url, keys, deep, content = self._pool.get_a_task(TPEnum.HTM_PARSE)

            # ----2----
            parse_state, url_list, save_list = self._worker.working(priority, url, keys, deep, content)

            # ----3----
            if parse_state > 0:
                self._pool.update_number_dict(TPEnum.HTM_PARSE_SUCC, +1)
                for _url, _keys, _priority in url_list:
                    self._pool.add_a_task(TPEnum.URL_FETCH, (_priority, self._pool.get_number_dict(TPEnum.COUNTER), _url, _keys, deep + 1, 0))
                for item in save_list:
                    self._pool.add_a_task(TPEnum.ITEM_SAVE, (url, keys, item))
            else:
                self._pool.update_number_dict(TPEnum.HTM_PARSE_FAIL, +1)

            # ----4----
            self._pool.finish_a_task(TPEnum.HTM_PARSE)
        else:
            # ----1----
            task_list = [self._pool.get_a_task(TPEnum.HTM_PARSE) for _ in range(self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT))]

            # ----2.1----
            pool = multiprocessing.Pool()
            result_list = [pool.apply_async(self._worker.working, args=(task[0], task[2], task[3], task[4], task[5])) for task in task_list]
            pool.close()

            # ----2.2----
            for index in range(len(task_list)):
                priority, counter, url, keys, deep, content = task_list[index]
                parse_state, url_list, save_list = result_list[index].get(timeout=None)

                # ----3----
                if parse_state > 0:
                    self._pool.update_number_dict(TPEnum.HTM_PARSE_SUCC, +1)
                    for _url, _keys, _priority in url_list:
                        self._pool.add_a_task(TPEnum.URL_FETCH, (_priority, self._pool.get_number_dict(TPEnum.COUNTER), _url, _keys, deep+1, 0))
                    for item in save_list:
                        self._pool.add_a_task(TPEnum.ITEM_SAVE, (url, keys, item))
                else:
                    self._pool.update_number_dict(TPEnum.HTM_PARSE_FAIL, +1)

                # ----4----
                self._pool.finish_a_task(TPEnum.HTM_PARSE)

        # ----5----
        return True
