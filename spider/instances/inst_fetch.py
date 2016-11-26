# _*_ coding: utf-8 _*_

"""
inst_fetch.py by xianhu
"""

import time
import random
import logging
import requests
from ..utilities import make_random_useragent, params_chack, return_check


class Fetcher(object):
    """
    class of Fetcher, must include function working() and url_fetch()
    """

    def __init__(self, normal_max_repeat=3, normal_sleep_time=3, critical_max_repeat=10, critical_sleep_time=10):
        """
        constructor
        """
        self.normal_max_repeat = normal_max_repeat          # default: 3, maximum repeat time for normal url
        self.normal_sleep_time = normal_sleep_time          # default: 3, sleeping time after a fetching for normal url
        self.critical_max_repeat = critical_max_repeat      # default: 10, maximum repeat time for critical url
        self.critical_sleep_time = critical_sleep_time      # default: 10, sleeping time after a fetching for critical url

        self.log_str_format = "keys=%s, critical=%s, fetch_repeat=%s, url=%s"
        return

    @params_chack(object, str, object, bool, int)
    def working(self, url, keys, critical, fetch_repeat):
        """
        working function, must "try, expect" and call self.url_fetch(), don't change parameters and return
        :return (code, content): code can be -1(fetch failed), 0(need repeat), 1(fetch success), content can be anything
        """
        logging.debug("%s start: %s", self.__class__.__name__, self.log_str_format % (keys, critical, fetch_repeat, url))

        time.sleep(random.randint(0, self.normal_sleep_time if (not critical) else self.critical_sleep_time))
        try:
            code, content = self.url_fetch(url, keys, critical, fetch_repeat)
        except Exception as excep:
            if ((not critical) and (fetch_repeat >= self.normal_max_repeat)) or (critical and (fetch_repeat >= self.critical_max_repeat)):
                code, content = -1, None
                logging.error("%s error: %s, %s", self.__class__.__name__, excep, self.log_str_format % (keys, critical, fetch_repeat, url))
            else:
                code, content = 0, None
                logging.debug("%s repeat: %s, %s", self.__class__.__name__, excep, self.log_str_format % (keys, critical, fetch_repeat, url))

        logging.debug("%s end: code=%s, url=%s", self.__class__.__name__, code, url)
        return code, content

    @return_check(int, object)
    def url_fetch(self, url, keys, critical, fetch_repeat):
        """
        fetch the content of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        # get response based on headers
        headers = {"User-Agent": make_random_useragent(), "Accept-Encoding": "gzip"}
        response = requests.get(url, params=None, data=None, headers=headers, cookies=None, timeout=(3.05, 10))
        if response.history:
            logging.debug("%s redirect: %s", self.__class__.__name__, self.log_str_format % (keys, critical, fetch_repeat, url))

        # get content(cur_code, cur_url, cur_html)
        content = (response.status_code, response.url, response.text)

        # return code, conten
        return 1, content
