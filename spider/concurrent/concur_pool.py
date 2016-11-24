# _*_ coding: utf-8 _*_

"""
concur_pool.py by xianhu
"""

import logging
import queue
import threading
import multiprocessing
from ..abcbase import BasePool
from ..abcbase import ParseProcess, SaveProcess
from ..abcbase import FetchThread, ParseThread, SaveThread, MonitorThread


class ConcurPool(BasePool):
    """
    class of ConcurPool, can be instanced to thread_pool or process_pool
    """

    def __init__(self, fetcher, parser, saver, url_filter=None, pool_type="thread", monitor_sleep_time=5):
        """
        constructor
        """
        BasePool.__init__(self, fetcher, parser, saver, pool_type=pool_type)
        self.url_filter = url_filter

        # define different variables based on self.pool_type
        if self.pool_type == "thread":
            self.fetch_queue = queue.PriorityQueue()
            self.parse_queue = queue.PriorityQueue()
            self.save_queue = queue.Queue()

            self.lock = threading.Lock()
        else:
            self.fetch_queue = multiprocessing.JoinableQueue()
            self.parse_queue = multiprocessing.JoinableQueue()
            self.save_queue = multiprocessing.JoinableQueue()

            self.manager = multiprocessing.Manager()
            self.number_dict = self.manager.dict(self.number_dict)
            self.lock = multiprocessing.Lock()

        # set monitor thread
        self.monitor_stop = False
        self.monitor = MonitorThread("monitor", self, sleep_time=monitor_sleep_time)
        self.monitor.setDaemon(True)
        self.monitor.start()
        return

    def start_work_and_wait_done(self, fetcher_num=10, parser_num=1, is_over=True):
        """
        start this pool, and wait for finishing
        """
        logging.warning("%s start: fetcher_num=%s, parser_num=%s, is_over=%s", self.pool_name, fetcher_num, parser_num, is_over)

        if self.pool_type == "thread":
            threads_list = [FetchThread("fetcher-%d" % i, self.inst_fetcher, self) for i in range(fetcher_num)] + \
                           [ParseThread("parser", self.inst_parser, self)] + \
                           [SaveThread("saver", self.inst_saver, self)]
            process_list = []
        else:
            threads_list = [FetchThread("fetcher-%d" % i, self.inst_fetcher, self) for i in range(fetcher_num)]
            process_list = [ParseProcess("parser-%d" % i, self.inst_parser, self) for i in range(parser_num)] + \
                           [SaveProcess("saver", self.inst_saver, self)]

        for thread in threads_list:
            thread.setDaemon(True)
            thread.start()

        for process in process_list:
            process.daemon = True
            process.start()

        for thread in threads_list:
            if thread.is_alive():
                thread.join()

        for process in process_list:
            if process.is_alive():
                process.join()

        if is_over and self.monitor.is_alive():
            self.monitor_stop = True
            self.monitor.join()

        logging.warning("%s end: fetcher_num=%s, parser_num=%s, is_over=%s", self.pool_name, fetcher_num, parser_num, is_over)
        return
