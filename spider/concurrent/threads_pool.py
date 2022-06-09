# _*_ coding: utf-8 _*_

"""
threads_pool.py by xianhu
"""

import copy
import queue
import logging
import threading

from .threads_inst import *
from ..instances import Fetcher, Parser, Saver, Proxieser
from ..utilities import UrlFilter, TaskFetch


class ThreadPool(object):
    """
    class of ThreadPool
    """

    def __init__(
            self, fetcher: Fetcher, parser: Parser = None, saver: Saver = None, proxieser: Proxieser = None,
            url_filter: UrlFilter = None, queue_parse_size=-1, queue_save_size=-1, queue_proxies_size=-1,
    ):
        """
        constructor, queue_parse_size/queue_save_size/queue_proxies_size are the maximum size of each queue, -1 to no limition
        """
        self._inst_fetcher = fetcher  # fetcher instance, subclass of Fetcher
        self._inst_parser = parser  # parser instance, subclass of Parser or None
        self._inst_saver = saver  # saver instance, subclass of Saver or None
        self._inst_proxieser = proxieser  # proxieser instance, subclass of Proxieser or None
        self._url_filter: UrlFilter = url_filter  # default: None, also can be UrlFilter()

        self._thread_fetcher_list = []  # fetcher threads list, define length in start_working()
        self._thread_parser = None  # parser thread, be None if no instance of parser
        self._thread_saver = None  # saver thread, be None if no instance of saver
        self._thread_proxieser = None  # proxieser thread, be None if no instance of proxieser
        self._thread_stop_flag = False  # default: False, stop flag of threads

        self._queue_fetch = queue.PriorityQueue(-1)  # TaskFetch(priority, keys, deep, url, repeat)
        self._queue_parse = queue.PriorityQueue(queue_parse_size)  # TaskParse(priority, keys, deep, url, content)
        self._queue_save = queue.PriorityQueue(queue_save_size)  # TaskSave(priority, keys, deep, url, item)
        self._queue_proxies = queue.Queue(queue_proxies_size)  # {"http": "http://auth@ip:port", "https": "https://auth@ip:port"}

        self._number_dict = {
            TPEnum.URL_FETCH_RUN: 0, TPEnum.URL_FETCH_NOT: 0, TPEnum.URL_FETCH_SUCC: 0, TPEnum.URL_FETCH_FAIL: 0,
            TPEnum.HTM_PARSE_RUN: 0, TPEnum.HTM_PARSE_NOT: 0, TPEnum.HTM_PARSE_SUCC: 0, TPEnum.HTM_PARSE_FAIL: 0,
            TPEnum.ITEM_SAVE_RUN: 0, TPEnum.ITEM_SAVE_NOT: 0, TPEnum.ITEM_SAVE_SUCC: 0, TPEnum.ITEM_SAVE_FAIL: 0,
            TPEnum.PROXIES_LEFT: 0, TPEnum.PROXIES_FAIL: 0,
        }
        self._lock = threading.Lock()

        self._thread_monitor = MonitorThread("monitor", self)
        self._thread_monitor.setDaemon(True)
        self._thread_monitor.start()
        logging.warning("ThreadPool has been initialized")
        return

    def set_start_task(self, task_fetch: TaskFetch):
        """
        set start task, according to a TaskFetch()
        """
        self.add_a_task(TPEnum.URL_FETCH, task_fetch)
        return

    def start_working(self, fetchers_num=10):
        """
        start this thread pool based on fetchers_num
        """
        logging.warning("ThreadPool starts working: urls_num=%s, fetchers_num=%s", self.get_number_dict(TPEnum.URL_FETCH_NOT), fetchers_num)
        self._thread_stop_flag = False

        self._thread_fetcher_list = [FetchThread("fetcher-%d" % (i + 1), copy.deepcopy(self._inst_fetcher), self) for i in range(fetchers_num)]
        self._thread_parser = ParseThread("parser", self._inst_parser, self) if self._inst_parser else None
        self._thread_saver = SaveThread("saver", self._inst_saver, self) if self._inst_saver else None
        self._thread_proxieser = ProxiesThread("proxieser", self._inst_proxieser, self) if self._inst_proxieser else None

        for thread_fetcher in self._thread_fetcher_list:
            thread_fetcher.setDaemon(True)
            thread_fetcher.start()

        if self._thread_parser:
            self._thread_parser.setDaemon(True)
            self._thread_parser.start()

        if self._thread_saver:
            self._thread_saver.setDaemon(True)
            self._thread_saver.start()

        if self._thread_proxieser:
            self._thread_proxieser.setDaemon(True)
            self._thread_proxieser.start()

        logging.warning("ThreadPool starts working successfully")
        return

    def wait_for_finished(self):
        """
        wait for finishing this thread pool
        """
        logging.warning("ThreadPool waits for finishing")
        self._thread_stop_flag = True

        for _thread_fetcher in filter(lambda x: x.is_alive(), self._thread_fetcher_list):
            _thread_fetcher.join()

        if self._thread_parser and self._thread_parser.is_alive():
            self._thread_parser.join()

        if self._thread_saver and self._thread_saver.is_alive():
            self._thread_saver.join()

        if self._thread_monitor and self._thread_monitor.is_alive():
            self._thread_monitor.join()

        logging.warning("ThreadPool has finished...")
        return self._number_dict

    def get_proxies_flag(self):
        """
        get proxies flag of this thread pool
        """
        return True if self._inst_proxieser else False

    def get_number_dict(self, key=None):
        """
        get value of self._number_dict based on key
        """
        return self._number_dict[key] if key else self._number_dict

    def update_number_dict(self, key, value):
        """
        update value of self._number_dict based on key
        """
        self._lock.acquire()
        self._number_dict[key] += value
        self._lock.release()
        return

    def is_ready_to_finish(self):
        """
        check state of this thread pool, return True if all tasks finished and self._thread_stop_flag is True
        """
        return False if self._number_dict[TPEnum.URL_FETCH_RUN] or self._number_dict[TPEnum.URL_FETCH_NOT] or \
                        self._number_dict[TPEnum.HTM_PARSE_RUN] or self._number_dict[TPEnum.HTM_PARSE_NOT] or \
                        self._number_dict[TPEnum.ITEM_SAVE_RUN] or self._number_dict[TPEnum.ITEM_SAVE_NOT] or \
                        (not self._thread_stop_flag) else True

    def add_a_task(self, task_type, task):
        """
        add a task based on task_type, also for proxies
        """
        if (task_type == TPEnum.URL_FETCH) and ((task.repeat > 0) or (not self._url_filter) or self._url_filter.check_and_add(task.url)):
            self._queue_fetch.put(task, block=False, timeout=None)
            self.update_number_dict(TPEnum.URL_FETCH_NOT, +1)
        elif (task_type == TPEnum.HTM_PARSE) and self._thread_parser:
            self._queue_parse.put(task, block=True, timeout=None)
            self.update_number_dict(TPEnum.HTM_PARSE_NOT, +1)
        elif (task_type == TPEnum.ITEM_SAVE) and self._thread_saver:
            self._queue_save.put(task, block=True, timeout=None)
            self.update_number_dict(TPEnum.ITEM_SAVE_NOT, +1)
        elif (task_type == TPEnum.PROXIES) and self._thread_proxieser:
            self._queue_proxies.put(task, block=True, timeout=None)
            self.update_number_dict(TPEnum.PROXIES_LEFT, +1)
        return

    def get_a_task(self, task_type):
        """
        get a task based on task_type, also for proxies
        """
        task = None
        if task_type == TPEnum.URL_FETCH:
            task = self._queue_fetch.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.URL_FETCH_NOT, -1)
            self.update_number_dict(TPEnum.URL_FETCH_RUN, +1)
        elif task_type == TPEnum.HTM_PARSE:
            task = self._queue_parse.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.HTM_PARSE_NOT, -1)
            self.update_number_dict(TPEnum.HTM_PARSE_RUN, +1)
        elif task_type == TPEnum.ITEM_SAVE:
            task = self._queue_save.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.ITEM_SAVE_NOT, -1)
            self.update_number_dict(TPEnum.ITEM_SAVE_RUN, +1)
        elif task_type == TPEnum.PROXIES:
            task = self._queue_proxies.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.PROXIES_LEFT, -1)
        return task

    def finish_a_task(self, task_type):
        """
        finish a task based on task_type, also for proxies
        """
        if task_type == TPEnum.URL_FETCH:
            self._queue_fetch.task_done()
            self.update_number_dict(TPEnum.URL_FETCH_RUN, -1)
        elif task_type == TPEnum.HTM_PARSE:
            self._queue_parse.task_done()
            self.update_number_dict(TPEnum.HTM_PARSE_RUN, -1)
        elif task_type == TPEnum.ITEM_SAVE:
            self._queue_save.task_done()
            self.update_number_dict(TPEnum.ITEM_SAVE_RUN, -1)
        elif task_type == TPEnum.PROXIES:
            self._queue_proxies.task_done()
        return
