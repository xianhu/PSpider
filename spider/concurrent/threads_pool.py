# _*_ coding: utf-8 _*_

"""
threads_pool.py by xianhu
"""

import copy
import queue
import logging
import threading
from .threads_inst import *
from ..utilities import check_url_legal


class ThreadPool(object):
    """
    class of ThreadPool
    """

    def __init__(self, fetcher, parser=None, saver=None, proxieser=None, url_filter=None, queue_parse_size=-1, queue_proxies_size=-1):
        """
        constructor
        """
        self._inst_fetcher = fetcher                                        # fetcher instance, subclass of Fetcher
        self._inst_parser = parser                                          # parser instance, subclass of Parser or None
        self._inst_saver = saver                                            # saver instance, subclass of Saver or None
        self._inst_proxieser = proxieser                                    # proxieser instance, subclass of Proxieser
        self._url_filter = url_filter                                       # default: None, also can be UrlFilter()

        self._thread_fetcher_list = []                                      # fetcher thread list
        self._thread_parser = None                                          # parser thread, be None if not parser
        self._thread_saver = None                                           # saver thread, be None if not saver
        self._thread_proxieser = None                                       # proxieser thread, be None if not proxieser

        self._thread_stop_flag = False                                      # default: False, stop flag of threads
        self._fetcher_number = 0                                            # default: 0, fetcher number in thread pool

        self._queue_fetch = queue.PriorityQueue(-1)                         # (priority, counter, url, keys, deep, repeat)
        self._queue_parse = queue.PriorityQueue(queue_parse_size)           # (priority, counter, url, keys, deep, content)
        self._queue_save = queue.Queue(-1)                                  # (url, keys, item), item can be anything
        self._queue_proxies = queue.Queue(queue_proxies_size)               # {"http": "http://auth@ip:port", "https": "https://auth@ip:port"}

        self._number_dict = {
            TPEnum.URL_COUNTER: 0,                                          # the count of urls which appeared in self._queue_fetch
            TPEnum.TASKS_RUNNING: 0,                                        # the count of tasks which are running

            TPEnum.URL_FETCH_NOT: 0,                                        # the count of urls which haven't been fetched
            TPEnum.URL_FETCH_SUCC: 0,                                       # the count of urls which have been fetched successfully
            TPEnum.URL_FETCH_FAIL: 0,                                       # the count of urls which have been fetched failed

            TPEnum.HTM_PARSE_NOT: 0,                                        # the count of urls which haven't been parsed
            TPEnum.HTM_PARSE_SUCC: 0,                                       # the count of urls which have been parsed successfully
            TPEnum.HTM_PARSE_FAIL: 0,                                       # the count of urls which have been parsed failed

            TPEnum.ITEM_SAVE_NOT: 0,                                        # the count of urls which haven't been saved
            TPEnum.ITEM_SAVE_SUCC: 0,                                       # the count of urls which have been saved successfully
            TPEnum.ITEM_SAVE_FAIL: 0,                                       # the count of urls which have been saved failed

            TPEnum.PROXIES_LEFT: 0,                                         # the count of proxies which are avaliable
            TPEnum.PROXIES_FAIL: 0,                                         # the count of proxies which are unavaliable
        }
        self._lock = threading.Lock()                                       # the lock which self._number_dict needs

        self._thread_monitor = MonitorThread("monitor", self)
        self._thread_monitor.setDaemon(True)
        self._thread_monitor.start()
        logging.warning("ThreadPool has been initialized")
        return

    def set_start_url(self, url, priority=0, keys=None, deep=0):
        """
        set start url based on "priority", "keys" and "deep", keys must be a dictionary, and repeat must be 0
        """
        assert check_url_legal(url), "set_start_url error, please pass legal url to this function"
        self.add_a_task(TPEnum.URL_FETCH, (priority, self.get_number_dict(TPEnum.URL_COUNTER), url, keys or {}, deep, 0))
        return

    def start_working(self, fetcher_num=10):
        """
        start this thread pool
        """
        logging.warning("ThreadPool starts working: urls_count=%s, fetcher_num=%s", self.get_number_dict(TPEnum.URL_FETCH_NOT), fetcher_num)

        self._thread_stop_flag = False
        self._fetcher_number = fetcher_num

        self._thread_fetcher_list = [FetchThread("fetcher-%d" % (i+1), copy.deepcopy(self._inst_fetcher), self) for i in range(fetcher_num)]
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

        logging.warning("ThreadPool starts working: success")
        return

    def wait_for_finished(self):
        """
        wait for the finished of this thread pool
        """
        logging.warning("ThreadPool waits for finishing")

        self._thread_stop_flag = True
        for thread_fetcher in filter(lambda x: x.is_alive(), self._thread_fetcher_list):
            thread_fetcher.join()

        if self._thread_parser and self._thread_parser.is_alive():
            self._thread_parser.join()

        if self._thread_saver and self._thread_saver.is_alive():
            self._thread_saver.join()

        if self._thread_monitor and self._thread_monitor.is_alive():
            self._thread_monitor.join()

        logging.warning("ThreadPool has finished")
        return self._number_dict

    def get_proxies_flag(self):
        """
        get proxies flag of this thread pool
        """
        return True if self._inst_proxieser else False

    def get_fetcher_number(self):
        """
        get fetcher number of this thread pool
        """
        return self._fetcher_number

    def get_thread_stop_flag(self):
        """
        get threads' stop flag of this thread pool
        """
        return self._thread_stop_flag

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

    def is_all_tasks_done(self):
        """
        check if all tasks are done, according to self._number_dict
        """
        return False if self._number_dict[TPEnum.TASKS_RUNNING] or self._number_dict[TPEnum.URL_FETCH_NOT] or \
                        self._number_dict[TPEnum.HTM_PARSE_NOT] or self._number_dict[TPEnum.ITEM_SAVE_NOT] else True

    def add_a_task(self, task_name, task):
        """
        add a task based on task_name, also for proxies
        """
        if (task_name == TPEnum.URL_FETCH) and ((task[-1] > 0) or (not self._url_filter) or self._url_filter.check_and_add(task[2])):
            self._queue_fetch.put(task, block=False)
            self.update_number_dict(TPEnum.URL_FETCH_NOT, +1)
            self.update_number_dict(TPEnum.URL_COUNTER, +1)
        elif (task_name == TPEnum.HTM_PARSE) and self._thread_parser:
            self._queue_parse.put(task, block=True, timeout=None)
            self.update_number_dict(TPEnum.HTM_PARSE_NOT, +1)
        elif (task_name == TPEnum.ITEM_SAVE) and self._thread_saver:
            self._queue_save.put(task, block=False)
            self.update_number_dict(TPEnum.ITEM_SAVE_NOT, +1)
        elif (task_name == TPEnum.PROXIES) and self._thread_proxieser:
            self._queue_proxies.put(task, block=True, timeout=None)
            self.update_number_dict(TPEnum.PROXIES_LEFT, +1)
        return

    def get_a_task(self, task_name):
        """
        get a task based on task_name, also for proxies
        """
        task = None
        if task_name == TPEnum.PROXIES:
            task = self._queue_proxies.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.PROXIES_LEFT, -1)
            return task
        if task_name == TPEnum.URL_FETCH:
            task = self._queue_fetch.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.URL_FETCH_NOT, -1)
        elif task_name == TPEnum.HTM_PARSE:
            task = self._queue_parse.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.HTM_PARSE_NOT, -1)
        elif task_name == TPEnum.ITEM_SAVE:
            task = self._queue_save.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.ITEM_SAVE_NOT, -1)
        self.update_number_dict(TPEnum.TASKS_RUNNING, +1)
        return task

    def finish_a_task(self, task_name):
        """
        finish a task based on task_name, also for proxies
        """
        if task_name == TPEnum.PROXIES:
            self._queue_proxies.task_done()
            return
        if task_name == TPEnum.URL_FETCH:
            self._queue_fetch.task_done()
        elif task_name == TPEnum.HTM_PARSE:
            self._queue_parse.task_done()
        elif task_name == TPEnum.ITEM_SAVE:
            self._queue_save.task_done()
        self.update_number_dict(TPEnum.TASKS_RUNNING, -1)
        return
