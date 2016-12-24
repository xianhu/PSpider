# _*_ coding: utf-8 _*_

"""
concur_async_insts.py by xianhu
"""

import re
import sys
import asyncio
import logging
import datetime
import aiohttp
from ..utilities import get_url_legal, make_random_useragent


class FetcherAsync(object):
    """
    class of FetcherAsync
    """

    def __init__(self, max_repeat=3, sleep_time=0, loop=None):
        """
        constructor
        """
        self._max_repeat = max_repeat   # default: 3, maximum repeat fetching time for a url
        self._sleep_time = sleep_time   # default: 0, sleeping time after a fetching for a url

        # session object to fetch the content of a url
        self._session = aiohttp.ClientSession(loop=loop or asyncio.get_event_loop(), headers={"User-Agent": make_random_useragent()})
        return

    def __del__(self):
        """
        destructor
        """
        self._session.close()
        return

    async def fetch(self, url: str, keys: object, repeat: int) -> (int, object):
        """
        fetch the content of a url, must "try, expect" and don't change parameters and return
        :return (fetch_result, content): fetch_result can be -1(fetch failed), 0(need repeat), 1(fetch success), content can be anything
        """
        logging.debug("Fetcher start: keys=%s, repeat=%s, url=%s", keys, repeat, url)

        try:
            response = await self._session.get(url, params=None, data=None, timeout=5)
            if response.history:
                logging.debug("Fetcher redirect: keys=%s, repeat=%s, url=%s", keys, repeat, url)

            fetch_result, content = 1, (response.status, response.url, await response.text())
            await response.release()
        except Exception as excep:
            if repeat >= self._max_repeat:
                fetch_result, content = -1, None
                logging.error("Fetcher error: %s, keys=%s, repeat=%s, url=%s", excep, keys, repeat, url)
            else:
                fetch_result, content = 0, None
                logging.debug("Fetcher repeat: %s, keys=%s, repeat=%s, url=%s", excep, keys, repeat, url)

        logging.debug("Fetcher end: fetch_result=%s, url=%s", fetch_result, url)
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
        logging.debug("Parser start: priority=%s, keys=%s, deep=%s, url=%s", priority, keys, deep, url)

        try:
            *_, cur_html = content

            parse_result, url_list = 1, []
            if (self._max_deep < 0) or (deep < self._max_deep):
                a_list = re.findall(r"<a[\w\W]+?href=\"(?P<url>[\w\W]{5,}?)\"[\w\W]*?>[\w\W]+?</a>", cur_html, flags=re.IGNORECASE)
                url_list = [(_url, keys, priority + 1) for _url in [get_url_legal(href, url) for href in a_list]]
            else:
                logging.debug("Parser stop parse urls: priority=%s, keys=%s, deep=%s, url=%s", priority, keys, deep, url)

            title = re.search(r"<title>(?P<title>[\w\W]+?)</title>", cur_html, flags=re.IGNORECASE)
            save_list = [(title.group("title"), datetime.datetime.now()), ] if title else []
        except Exception as excep:
            parse_result, url_list, save_list = -1, [], []
            logging.error("Parser error: %s, priority=%s, keys=%s, deep=%s, url=%s", excep, priority, keys, deep, url)

        logging.debug("Parser end: parse_result=%s, len(url_list)=%s, len(save_list)=%s, url=%s", parse_result, len(url_list), len(save_list), url)
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
        logging.debug("Saver start: keys=%s, url=%s", keys, url)

        try:
            self._save_pip.write("\t".join([url, str(keys)] + [str(i) for i in item]) + "\n")
            self._save_pip.flush()
            save_result = True
        except Exception as excep:
            save_result = False
            logging.error("Saver error: %s, keys=%s, url=%s", excep, keys, url)

        logging.debug("Saver end: save_result=%s, url=%s", save_result, url)
        return save_result
