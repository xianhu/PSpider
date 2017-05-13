# _*_ coding: utf-8 _*_

"""
inst_fetch.py by xianhu
"""

import random
import logging
import asyncio
import aiohttp
from ..utilities import make_random_useragent


class FetcherAsync(object):
    """
    class of FetcherAsync, must include function fetch()
    """

    def __init__(self, max_repeat=3, sleep_time=0):
        """
        constructor
        """
        self._max_repeat = max_repeat       # default: 3, maximum repeat fetching time for a url
        self._sleep_time = sleep_time       # default: 0, sleeping time after a fetching for a url

        self._session = None                # session object to fetch the content of a url
        return

    def init_session(self, loop):
        """
        initial self._session based on loop
        """
        if not self._session:
            self._session = aiohttp.ClientSession(loop=loop, headers={"User-Agent": make_random_useragent(), "Accept-Encoding": "gzip"})
        return

    def close_session(self):
        """
        close self._session object
        """
        if not self._session.closed:
            self._session.close()
        return

    async def fetch(self, url: str, keys: object, repeat: int) -> (int, object):
        """
        fetch the content of a url, must "try, expect" and don't change the parameters and return
        :return (fetch_result, content): fetch_result can be -1(fetch failed), 0(need repeat), 1(fetch success), content can be anything
        """
        logging.debug("%s start: keys=%s, repeat=%s, url=%s", self.__class__.__name__, keys, repeat, url)

        await asyncio.sleep(random.randint(0, self._sleep_time))
        try:
            response = await self._session.get(url, params=None, data=None, timeout=5)
            if response.history:
                logging.debug("%s redirect: keys=%s, repeat=%s, url=%s", self.__class__.__name__, keys, repeat, url)

            fetch_result, content = 1, (response.status, response.url, await response.text())
            await response.release()
        except Exception as excep:
            if repeat >= self._max_repeat:
                fetch_result, content = -1, None
                logging.error("%s error: %s, keys=%s, repeat=%s, url=%s", self.__class__.__name__, excep, keys, repeat, url)
            else:
                fetch_result, content = 0, None
                logging.debug("%s repeat: %s, keys=%s, repeat=%s, url=%s", self.__class__.__name__, excep, keys, repeat, url)

        logging.debug("%s end: fetch_result=%s, url=%s", self.__class__.__name__, fetch_result, url)
        return fetch_result, content
