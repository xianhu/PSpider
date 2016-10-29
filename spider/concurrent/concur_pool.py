# _*_ coding: utf-8 _*_

"""
concur_pool.py by xianhu
"""

import queue
import logging
import threading
import multiprocessing
from .concur_base import TPEnum
from .concur_insts import FetchThread, ParseThread, ParseProcess, SaveThread, SaveProcess, MonitorThread


class ConcurPool(object):
    """
    class of ConcurPool, can be instanced to thread_pool or process_pool
    """

    def __init__(self, fetcher, parser, saver, url_filter=None, monitor_sleep_time=5, pool_type="thread"):
        """
        constructor
        """
        assert pool_type in ("thread", "process"), "pool_type must be 'thread' or 'process'"
        self.pool_name = "ThreadPool" if pool_type == "thread" else "ProcessPool"
        self.pool_type = pool_type          # default: "thread", must be "thread" or "process", to identify pool type

        self.inst_fetcher = fetcher         # fetcher instance, for fetch thread or process
        self.inst_parser = parser           # parser instance, for parse thread or process
        self.inst_saver = saver             # saver instance, for save thread or process
        self.url_filter = url_filter        # default: None, also can be UrlFilter()

        self.number_dict = {
            TPEnum.TASKS_RUNNING: 0,        # the count of tasks which are running

            TPEnum.URL_FETCH: 0,            # the count of urls which have been fetched successfully
            TPEnum.HTM_PARSE: 0,            # the count of urls which have been parsed successfully
            TPEnum.ITEM_SAVE: 0,            # the count of urls which have been saved successfully

            TPEnum.URL_NOT_FETCH: 0,        # the count of urls which haven't been fetched
            TPEnum.HTM_NOT_PARSE: 0,        # the count of urls which haven't been parsed
            TPEnum.ITEM_NOT_SAVE: 0,        # the count of urls which haven't been saved
        }

        # define different variables based on self.pool_type
        if self.pool_type == "thread":
            self.fetch_queue = queue.PriorityQueue()                # (priority, url, keys, deep, critical, fetch_repeat, parse_repeat)
            self.parse_queue = queue.PriorityQueue()                # (priority, url, keys, deep, critical, fetch_repeat, parse_repeat, content)
            self.save_queue = queue.Queue()                         # (url, keys, item), item can be any type object
            self.lock = threading.Lock()                            # the lock which self.number_dict needs
        else:
            self.fetch_queue = multiprocessing.JoinableQueue()      # (priority, url, keys, deep, critical, fetch_repeat, parse_repeat)
            self.parse_queue = multiprocessing.JoinableQueue()      # (priority, url, keys, deep, critical, fetch_repeat, parse_repeat, content)
            self.save_queue = multiprocessing.JoinableQueue()       # (url, keys, item), item can be any type object

            self.manager = multiprocessing.Manager()                # use multiprocessing.Manager to share memory
            self.number_dict = self.manager.dict(self.number_dict)  # change self.number_dict based on self.manager
            self.lock = multiprocessing.Lock()                      # the lock which self.number_dict needs

        # set monitor thread
        self.monitor_stop = False
        self.monitor = MonitorThread("monitor", self, sleep_time=monitor_sleep_time)
        self.monitor.setDaemon(True)
        self.monitor.start()
        return

    def set_start_url(self, url, keys, priority=0, deep=0, critical=False):
        """
        set start url based on "keys", "priority", "deep" and "critical", fetch_repeat and parse_repeat must be 0
        :param keys: you can add some information to this url, and pass that to fetcher, parser or saver
        :param critical: the critical flag of this url, default False to identity that this url is normal, else this url is critical
        """
        logging.warning("%s set_start_url: keys=%s, priority=%s, deep=%s, critical=%s, url=%s", self.pool_name, keys, priority, deep, critical, url)
        self.add_a_task(TPEnum.URL_FETCH, (priority, url, keys, deep, critical, 0, 0))
        return

    def start_work_and_wait_done(self, fetcher_num=10, parser_num=1, is_over=True):
        """
        start this pool, and wait for finishing
        :param is_over: whether to stop monitor when this pool stop, default True
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

    def is_all_tasks_done(self):
        """
        check if all tasks are done in this pool, according to self.number_dict
        """
        return False if self.number_dict[TPEnum.TASKS_RUNNING] or self.number_dict[TPEnum.URL_NOT_FETCH] or \
                        self.number_dict[TPEnum.HTM_NOT_PARSE] or self.number_dict[TPEnum.ITEM_NOT_SAVE] else True

    def update_number_dict(self, key, value):
        """
        update self.number_dict of this pool. if value is 0, set self.number_dict[key] to value
        """
        self.lock.acquire()
        if value == 0:
            self.number_dict[key] = value
        else:
            self.number_dict[key] += value
        self.lock.release()
        return

    # ================================================================================================================================
    def add_a_task(self, task_name, task_content):
        """
        add a task based on task_name, if queue is full, blocking the queue
        """
        if task_name == TPEnum.URL_FETCH:
            if (task_content[-1] > 0) or (task_content[-2] > 0) or (not self.url_filter) or self.url_filter.check(task_content[1]):
                self.fetch_queue.put(task_content, block=True)
                self.update_number_dict(TPEnum.URL_NOT_FETCH, +1)
        elif task_name == TPEnum.HTM_PARSE:
            self.parse_queue.put(task_content, block=True)
            self.update_number_dict(TPEnum.HTM_NOT_PARSE, +1)
        elif task_name == TPEnum.ITEM_SAVE:
            self.save_queue.put(task_content, block=True)
            self.update_number_dict(TPEnum.ITEM_NOT_SAVE, +1)
        else:
            logging.error("%s add_a_task error: parameter[%s] is invalid", self.pool_name, task_name)
        return

    def get_a_task(self, task_name):
        """
        get a task based on task_name, if queue is empty, raise queue.Empty
        """
        task_content = None
        if task_name == TPEnum.URL_FETCH:
            task_content = self.fetch_queue.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.URL_NOT_FETCH, -1)
        elif task_name == TPEnum.HTM_PARSE:
            task_content = self.parse_queue.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.HTM_NOT_PARSE, -1)
        elif task_name == TPEnum.ITEM_SAVE:
            task_content = self.save_queue.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.ITEM_NOT_SAVE, -1)
        else:
            logging.error("%s get_a_task error: parameter[%s] is invalid", self.pool_name, task_name)
        self.update_number_dict(TPEnum.TASKS_RUNNING, +1)
        return task_content

    def finish_a_task(self, task_name):
        """
        finish a task based on task_name, call queue.task_done()
        """
        if task_name == TPEnum.URL_FETCH:
            self.fetch_queue.task_done()
        elif task_name == TPEnum.HTM_PARSE:
            self.parse_queue.task_done()
        elif task_name == TPEnum.ITEM_SAVE:
            self.save_queue.task_done()
        else:
            logging.error("%s finish_a_task error: parameter[%s] is invalid", self.pool_name, task_name)
        self.update_number_dict(TPEnum.TASKS_RUNNING, -1)
        return
    # ================================================================================================================================
