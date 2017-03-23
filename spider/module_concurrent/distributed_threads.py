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

    def __init__(self, fetcher, parser, saver, monitor_sleep_time=5):
        """
        constructor
        """
        ThreadPool.__init__(self, fetcher, parser, saver, monitor_sleep_time=monitor_sleep_time)

        # redis configures
        self.client = None          # redis client
        self.redis_key_1 = None     # redis key
        self.redis_key_2 = None     # redis key
        return

    def init_redis(self, host="localhost", port=6379, db=0, key_1="", key_2=""):
        """
        initial redis client
        """
        if not self.client:
            self.client = redis.Redis(host=host, port=port, db=db)
            self.redis_key_1 = key_1
            self.redis_key_2 = key_2
        return

    # ================================================================================================================================
    def add_a_task(self, task_name, task_content):
        """
        add a task based on task_name
        """
        if task_name == TPEnum.URL_FETCH:
            self.client.push()
        elif task_name == TPEnum.HTM_PARSE:
            self._parse_queue.put(task_content, block=True)
            self.update_number_dict(TPEnum.HTM_NOT_PARSE, +1)
        elif task_name == TPEnum.ITEM_SAVE:
            self._save_queue.put(task_content, block=True)
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
            self.client.get()
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
