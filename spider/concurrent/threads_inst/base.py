# _*_ coding: utf-8 _*_

"""
base.py by xianhu
"""

import enum
import time
import queue
import logging
import threading


class TPEnum(enum.Enum):
    """
    enum of TPEnum, to mark the status of the threads_pool
    """
    URL_FETCH = "url_fetch"
    URL_FETCH_RUN = "url_fetch_run"
    URL_FETCH_NOT = "url_fetch_not"
    URL_FETCH_SUCC = "url_fetch_succ"
    URL_FETCH_FAIL = "url_fetch_fail"

    HTM_PARSE = "htm_parse"
    HTM_PARSE_RUN = "htm_parse_run"
    HTM_PARSE_NOT = "htm_parse_not"
    HTM_PARSE_SUCC = "htm_parse_succ"
    HTM_PARSE_FAIL = "htm_parse_fail"

    ITEM_SAVE = "item_save"
    ITEM_SAVE_RUN = "item_save_run"
    ITEM_SAVE_NOT = "item_save_not"
    ITEM_SAVE_SUCC = "item_save_succ"
    ITEM_SAVE_FAIL = "item_save_fail"

    PROXIES = "proxies"
    PROXIES_LEFT = "proxies_left"
    PROXIES_FAIL = "proxies_fail"


class BaseThread(threading.Thread):
    """
    class of BaseThread, as base class of each thread
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        threading.Thread.__init__(self, name=name)
        self._worker = worker
        self._pool = pool
        return

    def run(self):
        """
        rewrite auto-running function
        """
        while True:
            try:
                if not self.working():
                    break
            except queue.Empty:
                if self._pool.is_ready_to_finish():
                    break
        return

    def working(self):
        """
        procedure of each thread, return True to continue, False to stop
        """
        raise NotImplementedError


# ===============================================================================================================================
def init_monitor(self, name, pool):
    """
    constructor of MonitorThread
    """
    BaseThread.__init__(self, name, None, pool)
    self._init_time = time.time()

    self._last_fetch_num = 0
    self._last_parse_num = 0
    self._last_save_num = 0
    return


def work_monitor(self):
    """
    procedure of MonitorThread, auto running, return False if you need stop thread
    """
    time.sleep(5)
    info_list = []

    fetch_run = self._pool.get_number_dict(TPEnum.URL_FETCH_RUN)
    fetch_not = self._pool.get_number_dict(TPEnum.URL_FETCH_NOT)
    fetch_succ = self._pool.get_number_dict(TPEnum.URL_FETCH_SUCC)
    fetch_fail = self._pool.get_number_dict(TPEnum.URL_FETCH_FAIL)
    fetch_temp = (fetch_succ + fetch_fail) - self._last_fetch_num
    self._last_fetch_num = fetch_succ + fetch_fail
    info_list.append(f"fetch: [RUN={fetch_run}, NOT={fetch_not}, SUCC={fetch_succ}, FAIL={fetch_fail}, {fetch_temp}/5s];")

    parse_run = self._pool.get_number_dict(TPEnum.HTM_PARSE_RUN)
    parse_not = self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT)
    parse_succ = self._pool.get_number_dict(TPEnum.HTM_PARSE_SUCC)
    parse_fail = self._pool.get_number_dict(TPEnum.HTM_PARSE_FAIL)
    parse_temp = (parse_succ + parse_fail) - self._last_parse_num
    self._last_parse_num = parse_succ + parse_fail
    info_list.append(f"parse: [RUN={parse_run}, NOT={parse_not}, SUCC={parse_succ}, FAIL={parse_fail}, {parse_temp}/5s];")

    save_run = self._pool.get_number_dict(TPEnum.ITEM_SAVE_RUN)
    save_not = self._pool.get_number_dict(TPEnum.ITEM_SAVE_NOT)
    save_succ = self._pool.get_number_dict(TPEnum.ITEM_SAVE_SUCC)
    save_fail = self._pool.get_number_dict(TPEnum.ITEM_SAVE_FAIL)
    save_temp = (save_succ + save_fail) - self._last_save_num
    self._last_save_num = save_succ + save_fail
    info_list.append(f"save: [RUN={save_run}, NOT={save_not}, SUCC={save_succ}, FAIL={save_fail}, {save_temp}/5s];")

    if self._pool.get_proxies_flag():
        proxies_left = self._pool.get_number_dict(TPEnum.PROXIES_LEFT)
        proxies_fail = self._pool.get_number_dict(TPEnum.PROXIES_FAIL)
        info_list.append(f"proxies: [LEFT={proxies_left}, FAIL={proxies_fail}];")

    info_list.append(f"total_seconds={int(time.time() - self._init_time)}")

    logging.warning(" ".join(info_list))
    return not self._pool.is_ready_to_finish()


MonitorThread = type("MonitorThread", (BaseThread,), dict(__init__=init_monitor, working=work_monitor))
