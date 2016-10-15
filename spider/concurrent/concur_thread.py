# _*_ coding: utf-8 _*_

"""
concur_thread.py by xianhu
"""

import queue
import logging
import threading
from .concur_base import BasePool
from .concur_insts import FetchThread, ParseThread, SaveThread, MonitorThread


class ThreadPool(BasePool):
    """
    class of ThreadPool, as the subclass of BasePool
    """

    def __init__(self, fetcher, parser, saver, url_filter=None, monitor_sleep_time=5):
        """
        constructor
        """
        BasePool.__init__(self, fetcher, parser, saver, url_filter=url_filter)

        # "overwirte" variables of base class
        self.fetch_queue = queue.PriorityQueue()
        self.parse_queue = queue.PriorityQueue()
        self.save_queue = queue.Queue()
        self.lock = threading.Lock()

        # set monitor thread
        self.monitor_stop = False
        self.monitor = MonitorThread("monitor", self, sleep_time=monitor_sleep_time)
        self.monitor.setDaemon(True)
        self.monitor.start()
        return

    def start_work_and_wait_done(self, fetcher_num=5, parser_num=1, is_over=True):
        """
        start this ThreadPool, and wait for finishing
        :param parser_num: this parameter doesn't work in this class
        """
        logging.warning("ThreadPool start: fetcher_num=%s, parser_num=%s, is_over=%s", fetcher_num, parser_num, is_over)

        threads = [FetchThread("fetcher-%d" % i, self.inst_fetcher, self) for i in range(fetcher_num)] + \
                  [ParseThread("parser", self.inst_parser, self)] + \
                  [SaveThread("saver", self.inst_saver, self)]

        for thread in threads:
            thread.setDaemon(True)
            thread.start()

        for thread in threads:
            if thread.is_alive():
                thread.join()

        if is_over and self.monitor.is_alive():
            self.monitor_stop = True
            self.monitor.join()

        logging.warning("ThreadPool end: fetcher_num=%s, parser_num=%s, is_over=%s", fetcher_num, parser_num, is_over)
        return
