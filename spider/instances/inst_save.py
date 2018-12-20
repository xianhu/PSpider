# _*_ coding: utf-8 _*_

"""
inst_save.py by xianhu
"""

import sys
import logging
from ..utilities import get_dict_buildin


class Saver(object):
    """
    class of Saver, must include function working()
    """

    def __init__(self, save_pipe=sys.stdout):
        """
        constructor
        :param save_pipe: default sys.stdout, also can be a file handler
        """
        self._save_pipe = save_pipe
        self._name = self.__class__.__name__
        return

    def working(self, url: str, keys: dict, item: (list, tuple)) -> int:
        """
        working function, must "try, except" and don't change the parameters and returns
        :return save_state: can be -1(save failed), 1(save success)
        """
        try:
            save_state = self.item_save(url, keys, item)
        except Exception as excep:
            save_state = -1
            logging.error("%s error: %s, keys=%s, url=%s", self._name, excep, get_dict_buildin(keys), url)

        return save_state

    def item_save(self, url: str, keys: dict, item: (list, tuple)) -> int:
        """
        save the item of a url, you must rewrite this function, parameters and returns refer to self.working()
        """
        raise NotImplementedError
