# _*_ coding: utf-8 _*_

"""
concur_async_insts.py by xianhu
"""

import re
import sys
import random
import logging
import asyncio
import datetime
import aiohttp
from ..utilities import get_url_legal, make_random_useragent


class FetcherAsync(object):
    """
    class of FetcherAsync
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
        close the session object of this class
        """
        if not self._session.closed:
            self._session.close()
        return

    async def fetch(self, url: str, keys: object, repeat: int) -> (int, object):
        """
        fetch the content of a url, must "try, expect" and don't change parameters and return
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


class ParserAsync(object):
    """
    class of ParserAsync
    """

    def __init__(self, max_deep=0):
        """
        constructor
        """
        self._max_deep = max_deep       # default: 0, if -1, spider will not stop until all urls are fetched
        return

    async def parse(self, priority: int, url: str, keys: object, deep: int, content: object) -> (int, list, list):
        """
        parse the content of a url, must "try, except" and don't change parameters and return
        :return (parse_result, url_list, save_list): parse_result can be -1(parse failed), 1(parse success)
        :return (parse_result, url_list, save_list): url_list is [(url, keys, priority), ...], save_list is [item, ...]
        """
        logging.debug("%s start: priority=%s, keys=%s, deep=%s, url=%s", self.__class__.__name__, priority, keys, deep, url)

        try:
            *_, cur_html = content

            parse_result, url_list = 1, []
            if (self._max_deep < 0) or (deep < self._max_deep):
                a_list = re.findall(r"<a[\w\W]+?href=\"(?P<url>[\w\W]{5,}?)\"[\w\W]*?>[\w\W]+?</a>", cur_html, flags=re.IGNORECASE)
                url_list = [(_url, keys, priority + 1) for _url in [get_url_legal(href, url) for href in a_list]]
            else:
                logging.debug("%s stop parse urls: priority=%s, keys=%s, deep=%s, url=%s", self.__class__.__name__, priority, keys, deep, url)

            title = re.search(r"<title>(?P<title>[\w\W]+?)</title>", cur_html, flags=re.IGNORECASE)
            save_list = [(title.group("title"), datetime.datetime.now()), ] if title else []
        except Exception as excep:
            parse_result, url_list, save_list = -1, [], []
            logging.error("%s error: %s, priority=%s, keys=%s, deep=%s, url=%s", self.__class__.__name__, excep, priority, keys, deep, url)

        logging.debug("%s end: parse_result=%s, len(url_list)=%s, len(save_list)=%s, url=%s", self.__class__.__name__, parse_result, len(url_list), len(save_list), url)
        return parse_result, url_list, save_list


class SaverAsync(object):
    """
    class of SaverAsync
    """

    def __init__(self,  save_pipe=sys.stdout):
        """
        constructor
        """
        self._save_pip = save_pipe      # default: sys.stdout, also can be a file handler
        return

    async def save(self, url: str, keys: object, item: object) -> bool:
        """
        save the item of a url, must "try, except" and don't change parameters and return
        :return save_result: True or False
        """
        logging.debug("%s start: keys=%s, url=%s", self.__class__.__name__, keys, url)

        try:
            self._save_pip.write("\t".join([url, str(keys)] + [str(i) for i in item]) + "\n")
            self._save_pip.flush()
            save_result = True
        except Exception as excep:
            save_result = False
            logging.error("%s error: %s, keys=%s, url=%s", self.__class__.__name__, excep, keys, url)

        logging.debug("%s end: save_result=%s, url=%s", self.__class__.__name__, save_result, url)
        return save_result
