# _*_ coding: utf-8 _*_

"""
threads_inst_base.py by xianhu
"""

import enum
import time
import queue
import logging
import threading
from ...utilities import extract_error_info


class TPEnum(enum.Enum):
    """
    enum of TPEnum, to mark the status of web_spider
    """
    TASKS_RUNNING = "tasks_running"         # flag of tasks_running

    URL_FETCH = "url_fetch"                 # flag of url_fetch
    HTM_PARSE = "htm_parse"                 # flag of htm_parse
    ITEM_SAVE = "item_save"                 # flag of item_save

    URL_NOT_FETCH = "url_not_fetch"         # flag of url_not_fetch
    HTM_NOT_PARSE = "htm_not_parse"         # flag of htm_not_parse
    ITEM_NOT_SAVE = "item_not_save"         # flag of item_not_save

    URL_FETCH_SUCC = "url_fetch_succ"       # flag of url_fetch_succ
    HTM_PARSE_SUCC = "htm_parse_succ"       # flag of htm_parse_succ
    ITEM_SAVE_SUCC = "item_save_succ"       # flag of item_save_succ

    URL_FETCH_FAIL = "url_fetch_fail"       # flag of url_fetch_fail
    HTM_PARSE_FAIL = "htm_parse_fail"       # flag of htm_parse_fail
    ITEM_SAVE_FAIL = "item_save_fail"       # flag of item_save_fail

    PROXIES = "proxies"                     # flag of proxies
    PROXIES_LEFT = "proxies_left"           # flag of proxies_left --> URL_NOT_FETCH
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

        self._worker = worker       # the worker of each thread
        self._pool = pool           # the pool of each thread
        return

    def run(self):
        """
        rewrite run function, auto running and must call self.work()
        """
        logging.debug("%s[%s] start......", self.__class__.__name__, self.getName())
        while True:
            try:
                if not self.working():
                    break
            except (queue.Empty, TypeError):
                # caused by queue.get() or eval()
                if self._pool.is_all_tasks_done():
                    break
            except Exception:
                logging.error("%s[%s] error: %s", self.__class__.__name__, self.getName(), extract_error_info())
                break
        logging.debug("%s[%s] end......", self.__class__.__name__, self.getName())
        return

    def working(self):
        """
        procedure of each thread, return True to continue, False to stop
        """
        raise NotImplementedError


# ===============================================================================================================================
def init_monitor_thread(self, name, pool, sleep_time=5):
    """
    constructor of MonitorThread
    """
    BaseThread.__init__(self, name, None, pool)

    self._sleep_time = sleep_time       # sleeping time in every loop
    self._init_time = time.time()       # initial time of this spider

    self._last_fetch_num = 0            # fetch number in last time
    self._last_parse_num = 0            # parse number in last time
    self._last_save_num = 0             # save number in last time
    return


def work_monitor(self):
    """
    monitor the pool, auto running, and return False if you need stop thread
    """
    time.sleep(self._sleep_time)
    info = "%s status: running_tasks=%s;" % (self._pool.__class__.__name__, self._pool.get_number_dict(TPEnum.TASKS_RUNNING))

    cur_not_fetch = self._pool.get_number_dict(TPEnum.URL_NOT_FETCH)
    cur_fetch_succ = self._pool.get_number_dict(TPEnum.URL_FETCH_SUCC)
    cur_fetch_fail = self._pool.get_number_dict(TPEnum.URL_FETCH_FAIL)
    cur_fetch_all = cur_fetch_succ + cur_fetch_fail
    info += " fetch:[NOT=%d, SUCC=%d, FAIL=%d, %d/(%ds)];" % \
            (cur_not_fetch, cur_fetch_succ, cur_fetch_fail, cur_fetch_all-self._last_fetch_num, self._sleep_time)
    self._last_fetch_num = cur_fetch_all

    cur_not_parse = self._pool.get_number_dict(TPEnum.HTM_NOT_PARSE)
    cur_parse_succ = self._pool.get_number_dict(TPEnum.HTM_PARSE_SUCC)
    cur_parse_fail = self._pool.get_number_dict(TPEnum.HTM_PARSE_FAIL)
    cur_parse_all = cur_parse_succ + cur_parse_fail
    info += " parse:[NOT=%d, SUCC=%d, FAIL=%d, %d/(%ds)];" % \
            (cur_not_parse, cur_parse_succ, cur_parse_fail, cur_parse_all-self._last_parse_num, self._sleep_time)
    self._last_parse_num = cur_parse_all

    cur_not_save = self._pool.get_number_dict(TPEnum.ITEM_NOT_SAVE)
    cur_save_succ = self._pool.get_number_dict(TPEnum.ITEM_SAVE_SUCC)
    cur_save_fail = self._pool.get_number_dict(TPEnum.ITEM_SAVE_FAIL)
    cur_save_all = cur_save_succ + cur_save_fail
    info += " save:[NOT=%d, SUCC=%d, FAIL=%d, %d/(%ds)];" % \
            (cur_not_save, cur_save_succ, cur_save_fail, cur_save_all-self._last_save_num, self._sleep_time)
    self._last_save_num = cur_save_all

    if self._pool.get_proxies_flag():
        info += " proxies:[LEFT=%d, FAIL=%d];" % \
                (self._pool.get_number_dict(TPEnum.PROXIES_LEFT), self._pool.get_number_dict(TPEnum.PROXIES_FAIL))

    info += " total_seconds=%d" % (time.time() - self._init_time)
    logging.warning(info)
    return self._pool.get_monitor_flag()


MonitorThread = type("MonitorThread", (BaseThread,), dict(__init__=init_monitor_thread, working=work_monitor))
