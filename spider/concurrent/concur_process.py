# _*_ coding: utf-8 _*_

"""
concur_process.py by xianhu
"""

import logging
import multiprocessing
from .concur_base import BasePool
from .concur_insts import FetchThread, MonitorThread, ParseProcess, SaveProcess


class ProcessPool(BasePool):
    """
    class of ProcessPool, as the subclass of BasePool
    """

    def __init__(self, fetcher, parser, saver, url_filter=None, monitor_sleep_time=5):
        """
        constructor
        """
        BasePool.__init__(self, fetcher, parser, saver, url_filter=url_filter)

        # use Manager to share memory
        self.manager = multiprocessing.Manager()

        # "overwirte" variables of base class
        self.fetch_queue = multiprocessing.JoinableQueue()
        self.parse_queue = multiprocessing.JoinableQueue()
        self.save_queue = multiprocessing.JoinableQueue()

        self.number_dict = self.manager.dict(self.number_dict)
        self.lock = multiprocessing.Lock()

        # set monitor thread
        self.monitor_stop = False
        self.monitor = MonitorThread("monitor", self, sleep_time=monitor_sleep_time)
        self.monitor.setDaemon(True)
        self.monitor.start()
        return

    def start_work_and_wait_done(self, fetcher_num=5, parser_num=1, is_over=True):
        """
        start this ProcessPool, and wait for finishing
        """
        logging.warning("ProcessPool start: fetcher_num=%s, parser_num=%s, is_over=%s", fetcher_num, parser_num, is_over)

        threads = [FetchThread("fetcher-%d" % i, self.inst_fetcher, self) for i in range(fetcher_num)]
        processes = [ParseProcess("parser-%d" % i, self.inst_parser, self) for i in range(parser_num)] + \
                    [SaveProcess("saver", self.inst_saver, self)]

        for thread in threads:
            thread.setDaemon(True)
            thread.start()

        for process in processes:
            process.daemon = True
            process.start()

        for thread in threads:
            if thread.is_alive():
                thread.join()

        for process in processes:
            if process.is_alive():
                process.join()

        if is_over and self.monitor.is_alive():
            self.monitor_stop = True
            self.monitor.join()

        logging.warning("ProcessPool end: fetcher_num=%s, parser_num=%s, is_over=%s", fetcher_num, parser_num, is_over)
        return
