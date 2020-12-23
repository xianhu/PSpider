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
    URL_FETCH = "url_fetch"                 # flag of url_fetch **
    URL_FETCH_RUN = "url_fetch_run"         # flag of url_fetch_run
    URL_FETCH_NOT = "url_fetch_not"         # flag of url_fetch_not
    URL_FETCH_SUCC = "url_fetch_succ"       # flag of url_fetch_succ
    URL_FETCH_FAIL = "url_fetch_fail"       # flag of url_fetch_fail

    HTM_PARSE = "htm_parse"                 # flag of htm_parse **
    HTM_PARSE_RUN = "htm_parse_run"         # flag of htm_parse_run
    HTM_PARSE_NOT = "htm_parse_not"         # flag of htm_parse_not
    HTM_PARSE_SUCC = "htm_parse_succ"       # flag of htm_parse_succ
    HTM_PARSE_FAIL = "htm_parse_fail"       # flag of htm_parse_fail

    ITEM_SAVE = "item_save"                 # flag of item_save **
    ITEM_SAVE_RUN = "item_save_run"         # flag of item_save_run
    ITEM_SAVE_NOT = "item_save_not"         # flag of item_save_not
    ITEM_SAVE_SUCC = "item_save_succ"       # flag of item_save_succ
    ITEM_SAVE_FAIL = "item_save_fail"       # flag of item_save_fail

    PROXIES = "proxies"                     # flag of proxies **
    PROXIES_LEFT = "proxies_left"           # flag of proxies_left
    PROXIES_FAIL = "proxies_fail"           # flag of proxies_fail


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
        rewrite run function, auto running and must call self.working()
        """
        while True:
            try:
                if not self.working():
                    break
            except queue.Empty:
                if self._pool.get_thread_stop_flag() and self._pool.is_all_tasks_done():
                    break
        return

    def working(self):
        """
        procedure of each thread, return True to continue, False to stop
        """
        raise NotImplementedError


# ===============================================================================================================================
def init_monitor_thread(self, name, pool):
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
    monitor the thread pool, auto running, and return False if you need stop thread
    """
    time.sleep(5)

    fetch_run = self._pool.get_number_dict(TPEnum.URL_FETCH_RUN)
    fetch_not = self._pool.get_number_dict(TPEnum.URL_FETCH_NOT)
    fetch_succ = self._pool.get_number_dict(TPEnum.URL_FETCH_SUCC)
    fetch_fail = self._pool.get_number_dict(TPEnum.URL_FETCH_FAIL)
    info = "fetch: [RUN=%d, NOT=%d, SUCC=%d, FAIL=%d, %d/5s];" % (
        fetch_run, fetch_not, fetch_succ, fetch_fail, (fetch_succ + fetch_fail) - self._last_fetch_num
    )
    self._last_fetch_num = fetch_succ + fetch_fail

    parse_run = self._pool.get_number_dict(TPEnum.HTM_PARSE_RUN)
    parse_not = self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT)
    parse_succ = self._pool.get_number_dict(TPEnum.HTM_PARSE_SUCC)
    parse_fail = self._pool.get_number_dict(TPEnum.HTM_PARSE_FAIL)
    info += " parse: [RUN=%d, NOT=%d, SUCC=%d, FAIL=%d, %d/5s];" % (
        parse_run, parse_not, parse_succ, parse_fail, (parse_succ + parse_fail) - self._last_parse_num
    )
    self._last_parse_num = parse_succ + parse_fail

    save_run = self._pool.get_number_dict(TPEnum.ITEM_SAVE_RUN)
    save_not = self._pool.get_number_dict(TPEnum.ITEM_SAVE_NOT)
    save_succ = self._pool.get_number_dict(TPEnum.ITEM_SAVE_SUCC)
    save_fail = self._pool.get_number_dict(TPEnum.ITEM_SAVE_FAIL)
    info += " save: [RUN=%d, NOT=%d, SUCC=%d, FAIL=%d, %d/5s];" % (
        save_run, save_not, save_succ, save_fail, (save_succ + save_fail) - self._last_save_num
    )
    self._last_save_num = save_succ + save_fail

    proxies_left = self._pool.get_number_dict(TPEnum.PROXIES_LEFT)
    proxies_fail = self._pool.get_number_dict(TPEnum.PROXIES_FAIL)
    if self._pool.get_proxies_flag():
        info += " proxies: [LEFT=%d, FAIL=%d];" % (proxies_left, proxies_fail)

    logging.warning(info + " total_seconds=%d" % (time.time() - self._init_time))
    return not (self._pool.get_thread_stop_flag() and self._pool.is_all_tasks_done())


MonitorThread = type("MonitorThread", (BaseThread, ), dict(__init__=init_monitor_thread, working=work_monitor))
