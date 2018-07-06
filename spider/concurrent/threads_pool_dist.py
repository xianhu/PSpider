# _*_ coding: utf-8 _*_

"""
threads_pool_dist.py by xianhu
"""

import redis
import logging
from .threads_inst import TPEnum
from .threads_pool import ThreadPool
from ..utilities import check_url_legal


class DistThreadPool(ThreadPool):
    """
    class of DistThreadPool, as the subclass of ThreadPool
    """

    def __init__(self, fetcher, parser=None, saver=None, proxieser=None, url_filter=None, monitor_sleep_time=5):
        """
        constructor
        """
        ThreadPool.__init__(self, fetcher, parser, saver, proxieser=proxieser, url_filter=url_filter, monitor_sleep_time=monitor_sleep_time)

        self._redis_client = None           # redis client object
        self._key_high_priority = None      # redis key, value is a urls list, which wait to fetch, high priority
        self._key_low_priority = None       # redis key, value is a urls list, which wait to fetch, low priority

        # make the spider run forever
        self.update_number_dict(TPEnum.URL_FETCH_NOT, -1)
        logging.info("%s has been initialized", self.__class__.__name__)
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

    # ================================================================================================================================
    def add_a_task(self, task_name, task_content):
        """
        add a task based on task_name, also for proxies
        """
        if task_name == TPEnum.URL_FETCH and check_url_legal(task_content[2]) and \
                ((task_content[-1] > 0) or (not self._url_filter) or self._url_filter.check_and_add(task_content[2])):
            self._redis_client.lpush(self._key_high_priority if task_content[0] < 100 else self._key_low_priority, task_content)
            self.update_number_dict(TPEnum.URL_FETCH_COUNT, +1)
        elif task_name == TPEnum.HTM_PARSE and self._thread_parser:
            self._queue_parse.put_nowait(task_content)
            self.update_number_dict(TPEnum.HTM_PARSE_NOT, +1)
        elif task_name == TPEnum.ITEM_SAVE and self._thread_saver:
            self._queue_save.put_nowait(task_content)
            self.update_number_dict(TPEnum.ITEM_SAVE_NOT, +1)
        elif task_name == TPEnum.PROXIES and self._thread_proxieser:
            self._queue_proxies.put_nowait(task_content)
            self.update_number_dict(TPEnum.PROXIES_LEFT, +1)
        return

    def get_a_task(self, task_name):
        """
        get a task based on task_name, also for proxies
        """
        task_content = None
        if task_name == TPEnum.PROXIES:
            task_content = self._queue_proxies.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.PROXIES_LEFT, -1)
            return task_content
        elif task_name == TPEnum.URL_FETCH:
            task_content = eval(self._redis_client.rpop(self._key_high_priority) or self._redis_client.rpop(self._key_low_priority))
        elif task_name == TPEnum.HTM_PARSE:
            task_content = self._queue_parse.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.HTM_PARSE_NOT, -1)
        elif task_name == TPEnum.ITEM_SAVE:
            task_content = self._queue_save.get(block=True, timeout=5)
            self.update_number_dict(TPEnum.ITEM_SAVE_NOT, -1)
        self.update_number_dict(TPEnum.TASKS_RUNNING, +1)
        return task_content

    def finish_a_task(self, task_name):
        """
        finish a task based on task_name, also for proxies
        """
        if task_name == TPEnum.PROXIES:
            self._queue_proxies.task_done()
            return
        elif task_name == TPEnum.URL_FETCH:
            pass
        elif task_name == TPEnum.HTM_PARSE:
            self._queue_parse.task_done()
        elif task_name == TPEnum.ITEM_SAVE:
            self._queue_save.task_done()
        self.update_number_dict(TPEnum.TASKS_RUNNING, -1)
        return
    # ================================================================================================================================
