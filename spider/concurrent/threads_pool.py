# _*_ coding: utf-8 _*_

"""
threads_pool.py by xianhu
"""

import copy
import queue
import logging
import threading
from .threads_inst import TPEnum, FetchThread, ParseThread, SaveThread, MonitorThread
from ..utilities import CONFIG_FETCH_MESSAGE


class ThreadPool(object):
    """
    class of ThreadPool
    """

    def __init__(self, fetcher, parser, saver, proxieser=None, url_filter=None, monitor_sleep_time=5):
        """
        constructor
        """
        self._inst_fetcher = fetcher                    # fetcher instance, subclass of Fetcher
        self._inst_parser = parser                      # parser instance, subclass of Parser
        self._inst_saver = saver                        # saver instance, subclass of Saver

        self._fetch_queue = queue.PriorityQueue()       # (priority, url, keys, deep, repeat)
        self._parse_queue = queue.PriorityQueue()       # (priority, url, keys, deep, content)
        self._save_queue = queue.Queue()                # (url, keys, item), item can be anything

        self._url_filter = url_filter                   # default: None, also can be UrlFilter()

        self._proxieser = proxieser                     # proxies instance, subclass of Proxieser
        self._proxies_queue = queue.Queue()             # {"http": "http://auth@ip:port", "https": "https://auth@ip:port"}

        self._number_dict = {
            TPEnum.TASKS_RUNNING: 0,                    # the count of tasks which are running

            TPEnum.URL_NOT_FETCH: 0,                    # the count of urls which haven't been fetched
            TPEnum.HTM_NOT_PARSE: 0,                    # the count of urls which haven't been parsed
            TPEnum.ITEM_NOT_SAVE: 0,                    # the count of urls which haven't been saved

            TPEnum.URL_FETCH_SUCC: 0,                   # the count of urls which have been fetched successfully
            TPEnum.HTM_PARSE_SUCC: 0,                   # the count of urls which have been parsed successfully
            TPEnum.ITEM_SAVE_SUCC: 0,                   # the count of urls which have been saved successfully

            TPEnum.URL_FETCH_FAIL: 0,                   # the count of urls which have been fetched failed
            TPEnum.HTM_PARSE_FAIL: 0,                   # the count of urls which have been parsed failed
            TPEnum.ITEM_SAVE_FAIL: 0,                   # the count of urls which have been saved failed

            TPEnum.PROXIES: 0,                          # the count of proxies which in self._proxies_queue
            TPEnum.PROXIES_FAIL: 0,                     # the count of proxies which banned by website
        }
        self._lock = threading.Lock()                   # the lock which self._number_dict needs

        # set monitor thread
        self._monitor_stop = False
        self._monitor = MonitorThread("monitor", self, sleep_time=monitor_sleep_time)
        self._monitor.setDaemon(True)
        self._monitor.start()
        return

    def set_start_url(self, url, priority=0, keys=None, deep=0):
        """
        set start url based on "priority", "keys" and "deep", repeat must be 0
        """
        self.add_a_task(TPEnum.URL_FETCH, (priority, url, keys, deep, 0))
        logging.debug("%s set_start_url: %s", self.__class__.__name__, CONFIG_FETCH_MESSAGE % (priority, keys, deep, 0, url))
        return

    def start_work_and_wait_done(self, fetcher_num=10, is_over=True):
        """
        start this pool, and wait for finishing
        """
        logging.warning("%s start: urls_count=%s, fetcher_num=%s, is_over=%s", self.__class__.__name__, self.get_number_dict(TPEnum.URL_NOT_FETCH), fetcher_num, is_over)

        # fetcher/parser/saver thread list
        fetcher_list = [FetchThread("fetcher-%d" % (i+1), copy.deepcopy(self._inst_fetcher), self) for i in range(fetcher_num)]
        parser_saver_list = [ParseThread("parser", self._inst_parser, self), SaveThread("saver", self._inst_saver, self)]

        # ----1----
        for thread in fetcher_list:
            thread.setDaemon(True)
            thread.start()

        # ----1----
        for thread in parser_saver_list:
            thread.setDaemon(True)
            thread.start()

        # ----2----
        for thread in fetcher_list:
            if thread.is_alive():
                thread.join()

        # clear the variables if all fetcher stoped
        while self.get_number_dict(TPEnum.URL_NOT_FETCH) > 0:
            priority, url, keys, deep, repeat = self.get_a_task(TPEnum.URL_FETCH)
            logging.ERROR("%s error: not fetch, %s", self.__class__.__name__, CONFIG_FETCH_MESSAGE % (priority, keys, deep, repeat, url))
            self.finish_a_task(TPEnum.URL_FETCH)

        # ----2----
        for thread in parser_saver_list:
            if thread.is_alive():
                thread.join()

        # ----3----
        if is_over and self._monitor.is_alive():
            self._monitor_stop = True
            self._monitor.join()

        logging.warning("%s end: fetcher_num=%s, is_over=%s, fetch:[SUCC=%d, FAIL=%d]; parse[SUCC=%d, FAIL=%d]; save:[SUCC=%d, FAIL=%d]",
                        self.__class__.__name__, fetcher_num, is_over,
                        self.get_number_dict(TPEnum.URL_FETCH_SUCC), self.get_number_dict(TPEnum.URL_FETCH_FAIL),
                        self.get_number_dict(TPEnum.HTM_PARSE_SUCC), self.get_number_dict(TPEnum.HTM_PARSE_FAIL),
                        self.get_number_dict(TPEnum.ITEM_SAVE_SUCC), self.get_number_dict(TPEnum.ITEM_SAVE_FAIL))
        return self._number_dict

    # ================================================================================================================================
    def get_monitor_stop_flag(self):
        """
        get the monitor stop flag of this pool
        """
        return self._monitor_stop

    def update_number_dict(self, key, value):
        """
        update the value of self._number_dict based on key
        """
        self._lock.acquire()
        self._number_dict[key] += value
        self._lock.release()
        return

    def get_number_dict(self, key):
        """
        get the value of self._number_dict based on key
        """
        return self._number_dict[key]

    def is_all_tasks_done(self):
        """
        check if all tasks are done, according to self._number_dict
        """
        return False if self._number_dict[TPEnum.TASKS_RUNNING] or self._number_dict[TPEnum.URL_NOT_FETCH] or \
                        self._number_dict[TPEnum.HTM_NOT_PARSE] or self._number_dict[TPEnum.ITEM_NOT_SAVE] else True

    # ================================================================================================================================
    def add_a_task(self, task_name, task_content):
        """
        add a task based on task_name
        """
        if task_name == TPEnum.URL_FETCH and ((task_content[-1] > 0) or (not self._url_filter) or self._url_filter.check_and_add(task_content[1])):
            self._fetch_queue.put_nowait(task_content)
            self.update_number_dict(TPEnum.URL_NOT_FETCH, +1)
        elif task_name == TPEnum.HTM_PARSE:
            self._parse_queue.put_nowait(task_content)
            self.update_number_dict(TPEnum.HTM_NOT_PARSE, +1)
        elif task_name == TPEnum.ITEM_SAVE:
            self._save_queue.put_nowait(task_content)
            self.update_number_dict(TPEnum.ITEM_NOT_SAVE, +1)
        return

    def get_a_task(self, task_name):
        """
        get a task based on task_name, if queue is empty, raise queue.Empty
        """
        task_content = None
        if task_name == TPEnum.URL_FETCH:
            task_content = self._fetch_queue.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.URL_NOT_FETCH, -1)
        elif task_name == TPEnum.HTM_PARSE:
            task_content = self._parse_queue.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.HTM_NOT_PARSE, -1)
        elif task_name == TPEnum.ITEM_SAVE:
            task_content = self._save_queue.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.ITEM_NOT_SAVE, -1)
        self.update_number_dict(TPEnum.TASKS_RUNNING, +1)
        return task_content

    def finish_a_task(self, task_name):
        """
        finish a task based on task_name, call queue.task_done()
        """
        if task_name == TPEnum.URL_FETCH:
            self._fetch_queue.task_done()
        elif task_name == TPEnum.HTM_PARSE:
            self._parse_queue.task_done()
        elif task_name == TPEnum.ITEM_SAVE:
            self._save_queue.task_done()
        self.update_number_dict(TPEnum.TASKS_RUNNING, -1)
        return
    # ================================================================================================================================
