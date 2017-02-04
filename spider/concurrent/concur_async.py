# _*_ coding: utf-8 _*_

"""
concur_async.py by xianhu
"""

import time
import asyncio
import logging
from .concur_abase import TPEnum, BasePool


class AsyncPool(BasePool):
    """
    class of AsyncPool, as the subclass of BasePool
    """

    def __init__(self, fetcher, parser, saver, url_filter=None, loop=None):
        """
        constructor
        """
        BasePool.__init__(self, url_filter=url_filter)

        self._loop = loop or asyncio.get_event_loop()           # event_loop from parameter or call asyncio.get_event_loop()
        self._queue = asyncio.PriorityQueue(loop=self._loop)    # (priority, url, keys, deep, repeat)

        self._fetcher = fetcher     # fetcher instance
        self._parser = parser       # parser instance
        self._saver = saver         # saver instance

        self._start_time = None     # start time of this pool
        return

    def start_work_and_wait_done(self, fetcher_num=10, is_over=True):
        """
        start this pool, and wait for finishing
        :param fetcher_num: the count of tasks
        :param is_over: not useful in this class
        """
        try:
            self._start_time = time.time()
            self._loop.run_until_complete(self._start(fetcher_num=fetcher_num))
        except KeyboardInterrupt as excep:
            logging.warning("%s start_work_and_wait_done keyboard interrupt: %s", self.__class__.__name__, excep)
        except Exception as excep:
            logging.error("%s start_work_and_wait_done error: %s", self.__class__.__name__, excep)
        finally:
            self._loop.stop()
            self._loop.run_forever()
            self._loop.close()
        return

    async def _start(self, fetcher_num):
        """
        start tasks, and wait for finishing
        """
        tasks_list = [asyncio.Task(self._work(index), loop=self._loop) for index in range(fetcher_num)]
        await self._queue.join()
        for task in tasks_list:
            task.cancel()
        self.print_status()
        return

    async def _work(self, index):
        """
        working process, fetching --> parsing --> saving
        """
        logging.warning("%s[worker-%s] start...", self.__class__.__name__, index)

        self._fetcher.init_session(self._loop)
        try:
            while True:
                # get a task
                priority, url, keys, deep, repeat = await self.get_a_task(task_name=TPEnum.URL_FETCH)

                # fetch the content of a url ================================================================
                fetch_result, content = await self._fetcher.fetch(url, keys, repeat)
                if fetch_result > 0:
                    self.update_number_dict(TPEnum.URL_FETCH, +1)                   # =======================

                    # parse the content of a url ============================================================
                    self.update_number_dict(TPEnum.HTM_NOT_PARSE, +1)
                    parse_result, url_list, save_list = await self._parser.parse(priority, url, keys, deep, content)
                    self.update_number_dict(TPEnum.HTM_NOT_PARSE, -1)

                    if parse_result > 0:
                        self.update_number_dict(TPEnum.HTM_PARSE, +1)               # =======================

                        # add new task to self._queue
                        for _url, _keys, _priority in url_list:
                            self.add_a_task(TPEnum.URL_FETCH, (_priority, _url, _keys, deep+1, 0))

                        # save the item of a url ============================================================
                        for item in save_list:
                            self.update_number_dict(TPEnum.ITEM_NOT_SAVE, +1)
                            save_result = await self._saver.save(url, keys, item)
                            self.update_number_dict(TPEnum.ITEM_NOT_SAVE, -1)

                            if save_result:
                                self.update_number_dict(TPEnum.ITEM_SAVE, +1)       # =======================
                elif fetch_result == 0:
                    self.add_a_task(TPEnum.URL_FETCH, (priority+1, url, keys, deep, repeat+1))
                else:
                    pass

                # finish a task
                self.finish_a_task(task_name=TPEnum.URL_FETCH)

                # print the information of this pool
                if self._number_dict[TPEnum.URL_FETCH] % 100 == 0:
                    self.print_status()
            # end of while True
        except asyncio.CancelledError:
            pass

        self._fetcher.close_session()
        logging.warning("%s[worker-%s] end...", self.__class__.__name__, index)
        return

    def update_number_dict(self, key, value):
        """
        update the value of self._number_dict based on key
        """
        self._number_dict[key] += value
        return

    def add_a_task(self, task_name, task_content):
        """
        add a task based on task_name, if queue is full, blocking the queue
        """
        if (task_content[-1] > 0) or (not self._url_filter) or self._url_filter.check_and_add(task_content[1]):
            self._queue.put_nowait(task_content)
            self.update_number_dict(TPEnum.URL_NOT_FETCH, +1)
        return

    async def get_a_task(self, task_name):
        """
        get a task based on task_name, if queue is empty, raise queue.Empty
        """
        task_content = await self._queue.get()
        self.update_number_dict(TPEnum.URL_NOT_FETCH, -1)
        self.update_number_dict(TPEnum.TASKS_RUNNING, +1)
        return task_content

    def finish_a_task(self, task_name):
        """
        finish a task based on task_name, call queue.task_done()
        """
        self._queue.task_done()
        self.update_number_dict(TPEnum.TASKS_RUNNING, -1)
        return

    def print_status(self):
        """
        print the information of this pool
        """
        info = "%s status: running_tasks=%s;" % (self.__class__.__name__, self._number_dict[TPEnum.TASKS_RUNNING])

        info += " fetch=(%d, %d);" % (self._number_dict[TPEnum.URL_NOT_FETCH], self._number_dict[TPEnum.URL_FETCH])
        info += " parse=(%d, %d);" % (self._number_dict[TPEnum.HTM_NOT_PARSE], self._number_dict[TPEnum.HTM_PARSE])
        info += " save=(%d, %d);" % (self._number_dict[TPEnum.ITEM_NOT_SAVE], self._number_dict[TPEnum.ITEM_SAVE])

        info += " total_seconds=%d" % (time.time() - self._start_time)
        logging.warning(info)
        return
