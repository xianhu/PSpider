# _*_ coding: utf-8 _*_

"""
concur_base.py by xianhu
"""

import enum
import queue
import logging
import threading
import multiprocessing


class TPEnum(enum.Enum):
    """
    enum of TPEnum, to express the status of web_spider
    """
    TASKS_RUNNING = "tasks_running"     # flag of tasks_running

    URL_FETCH = "url_fetch"             # flag of url_fetch
    HTM_PARSE = "htm_parse"             # flag of htm_parse
    ITEM_SAVE = "item_save"             # flag of item_save

    URL_NOT_FETCH = "url_not_fetch"     # flag of url_not_fetch
    HTM_NOT_PARSE = "htm_not_parse"     # flag of htm_not_parse
    ITEM_NOT_SAVE = "item_not_save"     # flag of item_not_save


class BaseConcur(object):
    """
    class of BaseConcur, as base class of BaseThread and BaseProcess
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        self.name = name        # the name of each thread or process
        self.worker = worker    # the worker of each thread or process
        self.pool = pool        # the thread_pool or process_pool
        return

    def run(self):
        """
        rewrite run function of Thread or Process, auto running, and must call self.work()
        """
        logging.warning("%s[%s] start", self.__class__.__name__, self.name)

        while True:
            try:
                if not self.work():
                    break
            except queue.Empty:
                if self.pool.is_all_tasks_done():
                    break

        logging.warning("%s[%s] end", self.__class__.__name__, self.name)
        return

    def work(self):
        """
        procedure of each thread or process, return True to continue, False to stop
        """
        assert False, "you must rewrite work function in subclass of %s" % self.__class__.__name__


class BaseThread(BaseConcur, threading.Thread):
    """
    class of BaseThread, as base class of each thread
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        threading.Thread.__init__(self, name=name)
        BaseConcur.__init__(self, name, worker, pool)
        return


class BaseProcess(BaseConcur, multiprocessing.Process):
    """
    class of BaseProcess, as base class of each process
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        multiprocessing.Process.__init__(self, name=name)
        BaseConcur.__init__(self, name, worker, pool)
        return
