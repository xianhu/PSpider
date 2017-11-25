# _*_ coding: utf-8 _*_

"""
inst_proxies.py by xianhu
"""

import logging
from ..utilities import extract_error_info


class Proxieser(object):
    """
    class of Proxieser, must include function working()
    """

    def working(self) -> list:
        """
        working function, must "try, except" and don't change the parameters and return
        :return (proxies_result, proxies_list): proxies_result can be -1(get success), 1(get failed)
        :return (proxies_result, proxies_list): proxies list getting from website or database
        """
        logging.debug("%s start", self.__class__.__name__)

        try:
            proxies_list = self.proxies_get()
        except Exception as excep:
            proxies_list = []
            logging.error("%s error: %s", self.__class__.__name__, extract_error_info(excep))

        logging.debug("%s end", self.__class__.__name__)
        return proxies_list

    def proxies_get(self) -> bool:
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        return True
