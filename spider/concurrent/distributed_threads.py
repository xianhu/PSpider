# _*_ coding: utf-8 _*_

"""
distributed_threads.py by xianhu
"""

import redis
import logging
from .concur_abase import TPEnum
from .concur_threads import ThreadPool


class DistThreadPool(ThreadPool):
    """
    class of DistThreadPool, as the subclass of ThreadPool
    """

    def __init__(self, fetcher, parser, saver, url_filter=None, monitor_sleep_time=5):
        """
        constructor
        """
        ThreadPool.__init__(self, fetcher, parser, saver, url_filter=url_filter, monitor_sleep_time=monitor_sleep_time)

        # redis configures
        self._client = None         # redis client object
        self._key_wait = None       # redis key, urls list, which wait to fetch
        self._key_all = None        # redis key, all urls set, the speed will be very slow because of too many urls

        # make the spider run forever
        self.update_number_dict(TPEnum.URL_NOT_FETCH, -1)
        return

    def init_redis(self, host="localhost", port=6379, db=0, key_wait="spider.wait", key_all="spider.all"):
        """
        initial redis client object
        """
        if not self._client:
            self._client = redis.Redis(host=host, port=port, db=db)
            self._key_wait = key_wait
            self._key_all = key_all
        return

    # ================================================================================================================================
    def add_a_task(self, task_name, task_content):
        """
        add a task based on task_name
        """
        if task_name == TPEnum.URL_FETCH:
            if (task_content[-1] > 0) or (
                ((not self._url_filter) or self._url_filter.check_and_add(task_content[1])) and
                ((not self._key_all) or self._client.sadd(self._key_all, task_content[1]))
            ):
                self._client.lpush(self._key_wait, task_content)
        elif task_name == TPEnum.HTM_PARSE:
            self._parse_queue.put_nowait(task_content)
            self.update_number_dict(TPEnum.HTM_NOT_PARSE, +1)
        elif task_name == TPEnum.ITEM_SAVE:
            self._save_queue.put_nowait(task_content)
            self.update_number_dict(TPEnum.ITEM_NOT_SAVE, +1)
        else:
            logging.error("%s add_a_task error: parameter task_name[%s] is invalid", self.__class__.__name__, task_name)
            exit()
        return

    def get_a_task(self, task_name):
        """
        get a task based on task_name, if queue is empty, raise queue.Empty
        """
        task_content = None
        if task_name == TPEnum.URL_FETCH:
            task_content = eval(self._client.brpop(self._key_wait, timeout=5)[1])
        elif task_name == TPEnum.HTM_PARSE:
            task_content = self._parse_queue.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.HTM_NOT_PARSE, -1)
        elif task_name == TPEnum.ITEM_SAVE:
            task_content = self._save_queue.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.ITEM_NOT_SAVE, -1)
        else:
            logging.error("%s get_a_task error: parameter task_name[%s] is invalid", self.__class__.__name__, task_name)
            exit()
        self.update_number_dict(TPEnum.TASKS_RUNNING, +1)
        return task_content

    def finish_a_task(self, task_name):
        """
        finish a task based on task_name, call queue.task_done()
        """
        if task_name == TPEnum.URL_FETCH:
            pass
        elif task_name == TPEnum.HTM_PARSE:
            self._parse_queue.task_done()
        elif task_name == TPEnum.ITEM_SAVE:
            self._save_queue.task_done()
        else:
            logging.error("%s finish_a_task error: parameter task_name[%s] is invalid", self.__class__.__name__, task_name)
            exit()
        self.update_number_dict(TPEnum.TASKS_RUNNING, -1)
        return
