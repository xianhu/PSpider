# _*_ coding: utf-8 _*_

"""
proxies.py by xianhu
"""

import logging
from .base import TPEnum, BaseThread


class ProxiesThread(BaseThread):
    """
    class of ProxiesThread, as the subclass of BaseThread
    """

    def working(self):
        """
        procedure of proxies, auto running, and return False if you need stop thread
        """
        # ----2----
        proxies_state, proxies_list = self._worker.working()

        # ----3----
        self._pool.accept_state_from_task(TPEnum.PROXIES, proxies_state, None)

        # ----4----
        for proxies in proxies_list:
            self._pool.add_a_task(TPEnum.PROXIES, proxies)
        if proxies_state <= 0:
            logging.warning("%s warning: %s", proxies_list[0], proxies_list[1])

        # ----6----
        return not (self._pool.get_thread_stop_flag() and self._pool.is_all_tasks_done())
