# _*_ coding: utf-8 _*_

"""
concur_abase.py by xianhu
"""

import enum
import queue
import logging
import threading


class TPEnum(enum.Enum):
    """
    enum of TPEnum, to express the status of web_spider
    """
    TASKS_RUNNING = "tasks_running"         # flag of tasks_running

    URL_FETCH = "url_fetch"                 # flag of url_fetch
    HTM_PARSE = "htm_parse"                 # flag of htm_parse
    ITEM_SAVE = "item_save"                 # flag of item_save

    URL_NOT_FETCH = "url_not_fetch"         # flag of url_not_fetch
    HTM_NOT_PARSE = "htm_not_parse"         # flag of htm_not_parse
    ITEM_NOT_SAVE = "item_not_save"         # flag of item_not_save

    URL_FETCH_SUCC = "url_fetch_succ"       # flag of url_fetch_succ
    HTM_PARSE_SUCC = "htm_parse_succ"       # flag of htm_parse_succ
    ITEM_SAVE_SUCC = "item_save_succ"       # flag of item_save_succ

    URL_FETCH_FAIL = "url_fetch_fail"       # flag of url_fetch_fail
    HTM_PARSE_FAIL = "htm_parse_fail"       # flag of htm_parse_fail
    ITEM_SAVE_FAIL = "item_save_fail"       # flag of item_save_fail


class BaseThread(threading.Thread):
    """
    class of BaseThread, as base class of each thread
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        threading.Thread.__init__(self, name=name)

        self._worker = worker       # the worker of each thread
        self._pool = pool           # the pool of each thread
        return

    def run(self):
        """
        rewrite run function, auto running and must call self.work()
        """
        logging.debug("%s[%s] start...", self.__class__.__name__, self.getName())

        while True:
            try:
                if not self.working():
                    break
            except queue.Empty:
                # caused by "queue.get()"
                if self._pool.is_all_tasks_done():
                    break
            except TypeError:
                # caused by "eval()" in distributed_threads.py
                if self._pool.is_all_tasks_done():
                    break
            except Exception as excep:
                logging.error("%s[%s] error: %s", self.__class__.__name__, self.getName(), excep)
                break

        logging.debug("%s[%s] end...", self.__class__.__name__, self.getName())
        return

    def working(self):
        """
        procedure of each thread, return True to continue, False to stop
        """
        raise NotImplementedError


class BasePool(object):
    """
    class of BasePool, as the base class of each pool
    """

    def __init__(self, fetcher, parser, saver, url_filter=None):
        """
        constructor
        """
        self._url_filter = url_filter       # default: None, also can be UrlFilter()

        self._inst_fetcher = fetcher        # fetcher instance
        self._inst_parser = parser          # parser instance
        self._inst_saver = saver            # saver instance

        self._number_dict = {
            TPEnum.TASKS_RUNNING: 0,        # the count of tasks which are running

            TPEnum.URL_NOT_FETCH: 0,        # the count of urls which haven't been fetched
            TPEnum.HTM_NOT_PARSE: 0,        # the count of urls which haven't been parsed
            TPEnum.ITEM_NOT_SAVE: 0,        # the count of urls which haven't been saved

            TPEnum.URL_FETCH_SUCC: 0,       # the count of urls which have been fetched successfully
            TPEnum.HTM_PARSE_SUCC: 0,       # the count of urls which have been parsed successfully
            TPEnum.ITEM_SAVE_SUCC: 0,       # the count of urls which have been saved successfully

            TPEnum.URL_FETCH_FAIL: 0,       # the count of urls which have been fetched failed
            TPEnum.HTM_PARSE_FAIL: 0,       # the count of urls which have been parsed failed
            TPEnum.ITEM_SAVE_FAIL: 0,       # the count of urls which have been saved failed
        }
        self._lock = threading.Lock()       # the lock which self._number_dict needs
        return

    def set_start_url(self, url, keys=None, priority=0, deep=0):
        """
        set start url based on "keys", "priority" and "deep", repeat must be 0
        """
        self.add_a_task(TPEnum.URL_FETCH, (priority, url, keys, deep, 0))
        logging.debug("%s set_start_url: keys=%s, priority=%s, deep=%s, url=%s", self.__class__.__name__, keys, priority, deep, url)
        return

    def start_work_and_wait_done(self, fetcher_num=10, is_over=True):
        """
        start this pool, and wait for finishing
        """
        raise NotImplementedError

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

    def add_a_task(self, task_name, task_content):
        """
        add a task based on task_name
        """
        raise NotImplementedError

    def get_a_task(self, task_name):
        """
        get a task based on task_name
        """
        raise NotImplementedError

    def finish_a_task(self, task_name):
        """
        finish a task based on task_name
        """
        raise NotImplementedError
