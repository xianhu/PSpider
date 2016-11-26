# _*_ coding: utf-8 _*_

"""
abc_base.py by xianhu
"""

import enum
import queue
import logging
import threading


class TPEnum(enum.Enum):
    """
    enum of TPEnum, to express the status of web_spider
    """
    TASKS_RUNNING = "tasks_running"     # flag of tasks_running

    URL_FETCH = "url_fetch"             # flag of url_fetched
    HTM_PARSE = "htm_parse"             # flag of htm_parsed
    ITEM_SAVE = "item_save"             # flag of item_saved

    URL_NOT_FETCH = "url_not_fetch"     # flag of url_not_fetch
    HTM_NOT_PARSE = "htm_not_parse"     # flag of htm_not_parse
    ITEM_NOT_SAVE = "item_not_save"     # flag of item_not_save


class BaseThread(threading.Thread):
    """
    class of BaseThread, as base class of each thread
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        threading.Thread.__init__(self, name=name)

        self.worker = worker        # the worker of each thread
        self.pool = pool            # the thread_pool of each thread
        return

    def run(self):
        """
        rewrite run function, auto running and must call self.work()
        """
        logging.warning("%s[%s] start", self.__class__.__name__, self.getName())

        while True:
            try:
                if not self.work():
                    break
            except queue.Empty:
                if self.pool.is_all_tasks_done():
                    break

        logging.warning("%s[%s] end", self.__class__.__name__, self.getName())
        return

    def work(self):
        """
        procedure of each thread, return True to continue, False to stop
        """
        assert False, "you must rewrite work function in %s" % self.__class__.__name__
