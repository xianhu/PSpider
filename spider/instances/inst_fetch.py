# _*_ coding: utf-8 _*_

"""
inst_fetch.py by xianhu
"""

import time
import random
import logging
import urllib.error
import urllib.request
from ..utilities import get_html_content, make_headers, make_referer_url, params_chack


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

        self.cookiejar = None                               # default: None, cookiejar for each fetcher
        self.opener = urllib.request                        # default: urllib.request, opener for each fetcher
        return

    @params_chack(object, str, object, bool, int)
    def working(self, url, keys, critical, fetch_repeat):
        """
        working function,  must "try, expect" and call self.url_fetch(), don't change parameters and returns
        :return (code, content): code can be -1(failed), 0(repeat), 1(success), content is a list or tuple
        """
        logging.debug("Fetcher start: keys=%s, critical=%s, fetch_repeat=%s, url=%s", keys, critical, fetch_repeat, url)

        time.sleep(random.randint(0, self.normal_sleep_time if (not critical) else self.critical_sleep_time))
        try:
            code, content = self.url_fetch(url, keys, critical, fetch_repeat)
        except Exception as excep:
            if ((not critical) and (fetch_repeat >= self.normal_max_repeat)) or (critical and (fetch_repeat >= self.critical_max_repeat)):
                code, content = -1, None
                logging.error("Fetcher error: %s, keys=%s, critical=%s, fetch_repeat=%s, url=%s", excep, keys, critical, fetch_repeat, url)
            else:
                code, content = 0, None
                logging.debug("Fetcher repeat: %s, keys=%s, critical=%s, fetch_repeat=%s, url=%s", excep, keys, critical, fetch_repeat, url)

        logging.debug("Fetcher end: code=%s, url=%s", code, url)
        return code, content

    def url_fetch(self, url, keys, critical, fetch_repeat):
        """
        fetch the content of a url, you can rewrite this function
        :return (code, content): code can be -1(failed), 0(repeat), 1(success), content is a list or tuple
        """
        # get response based on headers
        headers = make_headers(user_agent="all", referer=make_referer_url(url), accept_encoding="gzip")
        response = self.opener.urlopen(urllib.request.Request(url, data=None, headers=headers), timeout=10)

        # get content (cur_code, cur_url, cur_info, cur_html)
        cur_code, cur_url, cur_info = response.getcode(), response.geturl(), response.info()
        content = (cur_code, cur_url, cur_info, get_html_content(response, charset=None))
        if cur_url != url:
            logging.debug("Fetcher redirection: keys=%s, critical=%s, fetch_repeat=%s, %s,%s", keys, critical, fetch_repeat, cur_url, url)

        # return code, conten
        return 1, content
