# _*_ coding: utf-8 _*_

"""
concur_async.py by xianhu
"""

import re
import sys
import asyncio
import aiohttp
import logging
import datetime
from .abc_base import TPEnum, BasePool
from ..utilities import make_random_useragent, get_url_legal


class AsyncPool(BasePool):
    """
    class of AsyncPool, as the subclass of BasePool
    """

    def __init__(self, max_repeat=3, sleep_time=0, max_deep=1, save_pipe=sys.stdout, url_filter=None, loop=None):
        """
        constructor
        """
        BasePool.__init__(self, url_filter=url_filter)

        self.max_repeat = max_repeat                            # default: 3, maximum repeat fetching time for a url
        self.sleep_time = sleep_time                            # default: 0, sleeping time after a fetching for a url
        self.max_deep = max_deep                                # default: 0, if -1, spider will not stop until all urls are fetched
        self.save_pip = save_pipe

        self.loop = loop or asyncio.get_event_loop()            # event_loop from parameter or call get_event_loop()
        self.queue = asyncio.PriorityQueue(loop=self.loop)      # (priority, url, keys, deep, repeat)
        return

    def start_work_and_wait_done(self, fetcher_num=10, is_over=True):
        """
        start this pool, and wait for finishing
        """
        try:
            self.loop.run_until_complete(self._start(fetcher_num=fetcher_num))
        except KeyboardInterrupt as excep:
            logging.error("%s error: %s", excep)
        finally:
            self.loop.stop()
            self.loop.run_forever()
            self.loop.close()
        return

    async def _start(self, fetcher_num):
        """
        start this pool, and wait for finishing
        """
        tasks_list = [asyncio.Task(self.work(index), loop=self.loop) for index in range(fetcher_num)]
        await self.queue.join()
        for task in tasks_list:
            task.cancel()
        return

    async def work(self, index):
        """
        working process
        """
        logging.warning("Worker[%s] start", index)

        session = aiohttp.ClientSession(loop=self.loop)
        try:
            while True:
                priority, url, keys, deep, repeat = await self.queue.get()
                self.update_number_dict(TPEnum.URL_NOT_FETCH, -1)

                code, content = await self.fetch(session, url, keys, repeat)
                if code > 0:
                    self.update_number_dict(TPEnum.URL_FETCH, +1)

                    self.update_number_dict(TPEnum.HTM_NOT_PARSE, +1)
                    code, url_list, save_list = self.parse(priority, url, keys, deep, content)
                    self.update_number_dict(TPEnum.HTM_NOT_PARSE, -1)

                    if code > 0:
                        self.update_number_dict(TPEnum.HTM_PARSE, +1)

                        for _url, _keys, _priority in url_list:
                            self.add_a_task(TPEnum.URL_FETCH, (_priority, _url, _keys, deep+1, 0))

                        for item in save_list:
                            self.update_number_dict(TPEnum.ITEM_NOT_SAVE, +1)
                            result = self.save(url, keys, item)
                            self.update_number_dict(TPEnum.ITEM_NOT_SAVE, -1)

                            if result:
                                self.update_number_dict(TPEnum.ITEM_SAVE, +1)

                elif code == 0:
                    self.add_a_task(TPEnum.URL_FETCH, (priority, url, keys, deep, repeat+1))
                else:
                    pass

                self.queue.task_done()
        except asyncio.CancelledError:
            pass

        session.close()
        return

    async def fetch(self, session, url, keys, repeat):
        """
        fetch the content of a url
        :return (code, content): code can be -1(fetch failed), 0(need repeat), 1(fetch success), content can be anything
        """
        logging.debug("Fetcher start: keys=%s, repeat=%s, url=%s", keys, repeat, url)

        try:

            headers = {"User-Agent": make_random_useragent(), "Accept-Encoding": "gzip"}
            response = await session.get(url, allow_redirects=False, params=None, data=None, headers=headers, timeout=5)
            if response.history:
                logging.debug("Fetcher redirect: keys=%s, repeat=%s, url=%s", keys, repeat, url)

            code, content = 1, (response.status, response.url, await response.text())
            await response.release()
        except Exception as excep:
            if repeat >= self.max_repeat:
                code, content = -1, None
                logging.error("Fetcher error: %s, keys=%s, repeat=%s, url=%s", excep, keys, repeat, url)
            else:
                code, content = 0, None
                logging.debug("Fetcher repeat: %s, keys=%s, repeat=%s, url=%s", excep, keys, repeat, url)

        logging.debug("Fetcher end: code=%s, url=%s", code, url)
        return code, content

    def parse(self, priority, url, keys, deep, content):
        """
        parse the content
        """
        try:
            # parse content(cur_code, cur_url, cur_html)
            *_, cur_html = content

            # get url_list
            url_list = []
            if (self.max_deep < 0) or (deep < self.max_deep):
                a_list = re.findall(r"<a[\w\W]+?href=\"(?P<url>[\w\W]{5,}?)\"[\w\W]*?>[\w\W]+?</a>", cur_html, flags=re.IGNORECASE)
                url_list = [(_url, keys, priority + 1) for _url in [get_url_legal(href, url) for href in a_list]]
            else:
                logging.debug("%s stop parse urls: priority=%s, keys=%s, deep=%s, url=%s", self.__class__.__name__, priority, keys, deep, url)

            # get save_list
            title = re.search(r"<title>(?P<title>[\w\W]+?)</title>", cur_html, flags=re.IGNORECASE)
            save_list = [(url, title.group("title"), datetime.datetime.now()), ] if title else []
            code = 1
        except Exception as excep:
            code, url_list, save_list = -1, [], []
            logging.error("Parser error: %s, priority=%s, keys=%s, deep=%s, url=%s", excep, priority, keys, deep, url)

        # return code, url_list, save_list
        return code, url_list, save_list

    def save(self, url, keys, item):
        """
        save process
        """
        self.save_pip.write("\t".join([str(i) for i in item]) + "\n")
        self.save_pip.flush()
        return True

    def update_number_dict(self, key, value):
        """
        update number_dict of this pool
        """
        self.number_dict[key] += value
        return

    def add_a_task(self, task_name, task_content):
        """
        add a task based on task_name, if queue is full, blocking the queue
        """
        if (task_content[-1] > 0) or (not self.url_filter) or self.url_filter.check_and_add(task_content[1]):
            self.queue.put_nowait(task_content)
            self.update_number_dict(TPEnum.URL_NOT_FETCH, +1)
        return
