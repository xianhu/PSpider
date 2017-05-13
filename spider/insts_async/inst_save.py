# _*_ coding: utf-8 _*_

"""
inst_save.py by xianhu
"""

import sys
import logging


class SaverAsync(object):
    """
    class of SaverAsync, must include function save()
    """

    def __init__(self,  save_pipe=sys.stdout):
        """
        constructor
        """
        self._save_pip = save_pipe      # default: sys.stdout, also can be a file handler
        return

    async def save(self, url: str, keys: object, item: (list, tuple)) -> bool:
        """
        save the item of a url, must "try, except" and don't change the parameters and return
        :return save_result: True or False
        """
        logging.debug("%s start: keys=%s, url=%s", self.__class__.__name__, keys, url)

        try:
            self._save_pip.write("\t".join([url, str(keys)] + [str(i) for i in item]) + "\n")
            self._save_pip.flush()
            save_result = True
        except Exception as excep:
            save_result = False
            logging.error("%s error: %s, keys=%s, url=%s", self.__class__.__name__, excep, keys, url)

        logging.debug("%s end: save_result=%s, url=%s", self.__class__.__name__, save_result, url)
        return save_result
