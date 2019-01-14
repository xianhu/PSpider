# _*_ coding: utf-8 _*_

"""
inst_save.py by xianhu
"""

import sys


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
        return

    def working(self, url: str, keys: dict, item: (list, tuple)) -> (int, object):
        """
        working function, must "try, except" and don't change the parameters and returns
        :return save_state: can be -1(save failed), 1(save success)
        :return save_result: can be any object, or exception information[class_name, excep]
        """
        try:
            save_state, save_result = self.item_save(url, keys, item)
        except Exception as excep:
            save_state, save_result = -1, [self.__class__.__name__, str(excep)]

        return save_state, save_result

    def item_save(self, url: str, keys: dict, item: (list, tuple)) -> (int, object):
        """
        save the item of a url, you must overwrite this function, parameters and returns refer to self.working()
        """
        raise NotImplementedError
