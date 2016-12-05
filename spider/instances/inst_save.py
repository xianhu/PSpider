# _*_ coding: utf-8 _*_

"""
inst_save.py by xianhu
"""

import sys
import logging
from ..utilities import params_chack, return_check


class Saver(object):
    """
    class of Saver, must include function working()
    """

    def __init__(self, save_pipe=sys.stdout):
        """
        constructor
        """
        self.save_pipe = save_pipe      # default: sys.stdout, also can be a file handler
        return

    @params_chack(object, str, object, object)
    def working(self, url, keys, item):
        """
        working function, must "try, except" and don't change parameters and return
        :return result: True or False
        """
        logging.debug("%s start: keys=%s, url=%s", self.__class__.__name__, keys, url)

        try:
            result = self.item_save(url, keys, item)
        except Exception as excep:
            result = False
            logging.error("%s error: %s, keys=%s, url=%s", self.__class__.__name__, excep, keys, url)

        logging.debug("%s end: result=%s, url=%s", self.__class__.__name__, result, url)
        return result

    @return_check(bool)
    def item_save(self, url, keys, item):
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        self.save_pipe.write("\t".join([str(i) for i in item]) + "\n")
        self.save_pipe.flush()
        return True
