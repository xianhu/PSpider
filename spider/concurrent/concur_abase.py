# _*_ coding: utf-8 _*_

"""
concur_abase.py by xianhu
"""

import enum
import queue
import logging
import threading
from ..utilities import extract_error_info


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
        logging.debug("%s[%s] start...", self.__class__.__name__, self.getName())

        while True:
            try:
                if not self.working():
                    break
            except (queue.Empty, TypeError):
                # caused by "queue.get()" or "eval()"
                if self._pool.is_all_tasks_done():
                    break
            except Exception as excep:
                logging.error("%s[%s] error: %s", self.__class__.__name__, self.getName(), extract_error_info(excep))
                break

        logging.debug("%s[%s] end...", self.__class__.__name__, self.getName())
        return

    def working(self):
        """
        procedure of each thread, return True to continue, False to stop
        """
        raise NotImplementedError
