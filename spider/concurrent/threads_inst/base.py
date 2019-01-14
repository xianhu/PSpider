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
    URL_COUNTER = "url_counter"             # flag of url_counter, for priority_queue
    TASKS_RUNNING = "tasks_running"         # flag of tasks_running

    URL_FETCH = "url_fetch"                 # flag of url_fetch **
    URL_FETCH_NOT = "url_fetch_not"         # flag of url_fetch_not
    URL_FETCH_SUCC = "url_fetch_succ"       # flag of url_fetch_succ
    URL_FETCH_FAIL = "url_fetch_fail"       # flag of url_fetch_fail

    HTM_PARSE = "htm_parse"                 # flag of htm_parse **
    HTM_PARSE_NOT = "htm_parse_not"         # flag of htm_parse_not
    HTM_PARSE_SUCC = "htm_parse_succ"       # flag of htm_parse_succ
    HTM_PARSE_FAIL = "htm_parse_fail"       # flag of htm_parse_fail

    ITEM_SAVE = "item_save"                 # flag of item_save **
    ITEM_SAVE_NOT = "item_save_not"         # flag of item_save_not
    ITEM_SAVE_SUCC = "item_save_succ"       # flag of item_save_succ
    ITEM_SAVE_FAIL = "item_save_fail"       # flag of item_save_fail

    PROXIES = "proxies"                     # flag of proxies **
    PROXIES_LEFT = "proxies_left"           # flag of proxies_left --> URL_FETCH_NOT
    PROXIES_FAIL = "proxies_fail"           # flag of proxies_fail --> URL_FETCH_FAIL


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
            except Exception as excep:
                logging.error("%s[%s] error: %s", self.__class__.__name__, self.getName(), excep)
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
    info = "running_tasks=%s;" % self._pool.get_number_dict(TPEnum.TASKS_RUNNING)

    cur_fetch_not = self._pool.get_number_dict(TPEnum.URL_FETCH_NOT)
    cur_fetch_succ = self._pool.get_number_dict(TPEnum.URL_FETCH_SUCC)
    cur_fetch_fail = self._pool.get_number_dict(TPEnum.URL_FETCH_FAIL)
    cur_fetch_all = cur_fetch_succ + cur_fetch_fail
    info += " fetch:[NOT=%d, SUCC=%d, FAIL=%d, %d/5s];" % (cur_fetch_not, cur_fetch_succ, cur_fetch_fail, cur_fetch_all - self._last_fetch_num)
    self._last_fetch_num = cur_fetch_all

    cur_parse_not = self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT)
    cur_parse_succ = self._pool.get_number_dict(TPEnum.HTM_PARSE_SUCC)
    cur_parse_fail = self._pool.get_number_dict(TPEnum.HTM_PARSE_FAIL)
    cur_parse_all = cur_parse_succ + cur_parse_fail
    info += " parse:[NOT=%d, SUCC=%d, FAIL=%d, %d/5s];" % (cur_parse_not, cur_parse_succ, cur_parse_fail, cur_parse_all - self._last_parse_num)
    self._last_parse_num = cur_parse_all

    cur_save_not = self._pool.get_number_dict(TPEnum.ITEM_SAVE_NOT)
    cur_save_succ = self._pool.get_number_dict(TPEnum.ITEM_SAVE_SUCC)
    cur_save_fail = self._pool.get_number_dict(TPEnum.ITEM_SAVE_FAIL)
    cur_save_all = cur_save_succ + cur_save_fail
    info += " save:[NOT=%d, SUCC=%d, FAIL=%d, %d/5s];" % (cur_save_not, cur_save_succ, cur_save_fail, cur_save_all - self._last_save_num)
    self._last_save_num = cur_save_all

    if self._pool.get_proxies_flag():
        info += " proxies:[LEFT=%d, FAIL=%d];" % (self._pool.get_number_dict(TPEnum.PROXIES_LEFT), self._pool.get_number_dict(TPEnum.PROXIES_FAIL))

    logging.warning(info + " total_seconds=%d" % (time.time() - self._init_time))
    return not (self._pool.get_thread_stop_flag() and self._pool.is_all_tasks_done())


MonitorThread = type("MonitorThread", (BaseThread, ), dict(__init__=init_monitor_thread, working=work_monitor))
