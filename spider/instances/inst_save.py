# _*_ coding: utf-8 _*_

"""
inst_save.py by xianhu
"""

import sys
import logging
from ..utilities import params_chack, return_check


class Saver(object):
    """
    class of Saver, must include function working() and item_save()
    """

    def __init__(self, file_name=None):
        """
        constructor
        """
        self.save_num = 0               # initial: 0, count of items which have been saved successfully
        self.file_name = file_name      # default: None, output file or sys.stdout(if file_name is None)
        self.save_pipe = open(file_name, "w", encoding="utf-8") if file_name else sys.stdout
        return

    @params_chack(object, str, object, object)
    def working(self, url, keys, item):
        """
        working function, must "try, except" and call self.item_save(), don't change parameters and return
        :param keys: some information of this url, which can be used in this function
        :param item: the item of this url, which needs to be saved
        :return result: True or False
        """
        logging.debug("Saver start: keys=%s, url=%s", keys, url)

        try:
            result = self.item_save(url, keys, item)
            self.save_num += 1
        except Exception as excep:
            result = False
            logging.error("Saver error: %s, keys=%s, url=%s", excep, keys, url)

        logging.debug("Saver end: result=%s, url=%s", result, url)
        return result

    @return_check(bool)
    def item_save(self, url, keys, item):
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        self.save_pipe.write("\t".join([url, str(keys), "\t".join([str(i) for i in item])]) + "\n")
        self.save_pipe.flush()
        return True
