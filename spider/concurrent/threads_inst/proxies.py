# _*_ coding: utf-8 _*_

"""
proxies.py by xianhu
"""

import logging

from .base import TPEnum, BaseThread
from ...utilities import ResultProxies


class ProxiesThread(BaseThread):
    """
    class of ProxiesThread, as the subclass of BaseThread
    """

    def working(self):
        """
        procedure of proxies, auto running, return False if you need stop thread
        """
        # ----2----
        result: ResultProxies = self._worker.working()

        # ----3----
        if result.state_code > 0:
            for proxies in result.proxies_list:
                self._pool.add_a_task(TPEnum.PROXIES, proxies)
        else:
            logging.warning("%s warning: %s", result.excep_class, result.excep_string)

        # return
        return not self._pool.is_ready_to_finish()
