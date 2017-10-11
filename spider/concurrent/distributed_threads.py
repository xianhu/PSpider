# _*_ coding: utf-8 _*_

"""
distributed_threads.py by xianhu
"""

import redis
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
        self._redis_client = None           # redis client object
        self._key_high_priority = None      # redis key, value is a urls list, which wait to fetch, high priority
        self._key_low_priority = None       # redis key, value is a urls list, which wait to fetch, low priority

        # make the spider run forever
        self.update_number_dict(TPEnum.URL_NOT_FETCH, -1)
        return

    def init_redis(self, host="localhost", port=6379, db=0, key_high_priority="spider.high", key_low_priority="spider.low"):
        """
        initial redis client object
        """
        if not self._redis_client:
            self._redis_client = redis.Redis(host=host, port=port, db=db)
            self._key_high_priority = key_high_priority
            self._key_low_priority = key_low_priority
        return

    def set_start_url(self, url, keys=None, priority=0, deep=0):
        """
        ignore this function
        """
        raise NotImplementedError

    # ================================================================================================================================
    def add_a_task(self, task_name, task_content):
        """
        add a task based on task_name
        """
        if task_name == TPEnum.URL_FETCH and ((task_content[-1] > 0) or (not self._url_filter) or self._url_filter.check(task_content[1])):
            if task_content[0] < 5:
                self._redis_client.lpush(self._key_high_priority, task_content)
            else:
                self._redis_client.lpush(self._key_low_priority, task_content)
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
            task_content = eval(self._redis_client.rpop(self._key_high_priority) or self._redis_client.rpop(self._key_low_priority))
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
        if task_name == TPEnum.HTM_PARSE:
            self._parse_queue.task_done()
        elif task_name == TPEnum.ITEM_SAVE:
            self._save_queue.task_done()
        self.update_number_dict(TPEnum.TASKS_RUNNING, -1)
        return
