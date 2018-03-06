# _*_ coding: utf-8 _*_

"""
threads_inst_parse.py by xianhu
"""

from .threads_inst_base import TPEnum, BaseThread


class ParseThread(BaseThread):
    """
    class of ParseThread, as the subclass of BaseThread
    """

    def working(self):
        """
        procedure of parsing, auto running, and return True
        """
        # ----1----
        priority, counter, url, keys, deep, content = self._pool.get_a_task(TPEnum.HTM_PARSE)

        # ----2----
        parse_result, url_list, save_list = self._worker.working(priority, url, keys, deep, content)

        # ----3----
        if parse_result > 0:
            self._pool.update_number_dict(TPEnum.HTM_PARSE_SUCC, +1)
            for _url, _keys, _priority in url_list:
                self._pool.add_a_task(TPEnum.URL_FETCH, (_priority, self._pool.get_number_dict(TPEnum.URL_FETCH_COUNT), _url, _keys, deep+1, 0))
            for item in save_list:
                self._pool.add_a_task(TPEnum.ITEM_SAVE, (url, keys, item))
        else:
            self._pool.update_number_dict(TPEnum.HTM_PARSE_FAIL, +1)

        # ----4----
        self._pool.finish_a_task(TPEnum.HTM_PARSE)

        # ----5----
        return True
