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
        self.pool = pool        # thread_pool or process_pool
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


class BasePool(object):
    """
    class of BasePool, as base class of thread_pool or process_pool
    """

    def __init__(self, fetcher, parser, saver, url_filter=None):
        """
        constructor
        """
        self.inst_fetcher = fetcher         # fetcher instance, for fetch thread or process
        self.inst_parser = parser           # parser instance, for parse thread or process
        self.inst_saver = saver             # saver instance, for save thread or process
        self.url_filter = url_filter        # default: None, also can be UrlFilter()

        self.fetch_queue = None             # (priority, url, keys, deep, critical, fetch_repeat, parse_repeat)
        self.parse_queue = None             # (priority, url, keys, deep, critical, fetch_repeat, parse_repeat, content)
        self.save_queue = None              # (url, keys, item), item is an instance of Item()

        self.number_dict = {
            TPEnum.TASKS_RUNNING: 0,        # the count of tasks which are running

            TPEnum.URL_FETCH: 0,            # the count of urls which have been fetched successfully
            TPEnum.HTM_PARSE: 0,            # the count of urls which have been parsed successfully
            TPEnum.ITEM_SAVE: 0,            # the count of urls which have been saved successfully

            TPEnum.URL_NOT_FETCH: 0,        # the count of urls which haven't been fetched
            TPEnum.HTM_NOT_PARSE: 0,        # the count of urls which haven't been parsed
            TPEnum.ITEM_NOT_SAVE: 0,        # the count of urls which haven't been saved
        }
        self.lock = None                    # the lock which self.num_dict needs, rewrite in subclass
        return

    def set_start_url(self, url, keys, priority=0, deep=0, critical=False):
        """
        set start url based on "keys", "priority", "deep" and "critical", fetch_repeat and parse_repeat must be 0
        :param keys: you can add some information to this url, and pass that to fetcher, parser or saver
        :param critical: the critical flag of this url, default False to identity that this url is normal, else this url is critical
        """
        logging.warning("%s set_start_url: keys=%s, priority=%s, deep=%s, critical=%s, url=%s",
                        self.__class__.__name__, keys, priority, deep, critical, url)
        self.add_a_task(TPEnum.URL_FETCH, (priority, url, keys, deep, critical, 0, 0))
        return

    def start_work_and_wait_done(self, fetcher_num, parser_num, is_over=True):
        """
        start this pool, and wait for finishing. you must rewrite this funtion in subclass
        :param is_over: whether to stop monitor when this pool stop, default True
        """
        raise NotImplementedError

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
            logging.error("%s add_a_task error: parameter[%s] is invalid", self.__class__.__name__, task_name)
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
            logging.error("%s get_a_task error: parameter[%s] is invalid", self.__class__.__name__, task_name)
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
            logging.error("%s finish_a_task error: parameter[%s] is invalid", self.__class__.__name__, task_name)
        self.update_number_dict(TPEnum.TASKS_RUNNING, -1)
        return
    # ================================================================================================================================
