# _*_ coding: utf-8 _*_

"""
util_urlfilter.py by xianhu
"""

import re
from pybloom_live import ScalableBloomFilter
from .util_config import CONFIG_URL_LEGAL_PATTERN, CONFIG_URL_ILLEGAL_PATTERN


class UrlFilter(object):
    """
    class of UrlFilter, to filter url by regexs and (bloomfilter or set)
    """

    def __init__(self, black_patterns=(CONFIG_URL_ILLEGAL_PATTERN,), white_patterns=(CONFIG_URL_LEGAL_PATTERN,), capacity=None):
        """
        constructor, use the instance of BloomFilter if capacity else the instance of set
        """
        self._re_black_list = [re.compile(pattern, flags=re.IGNORECASE) for pattern in black_patterns] if black_patterns else []
        self._re_white_list = [re.compile(pattern, flags=re.IGNORECASE) for pattern in white_patterns] if white_patterns else []
        self._urlfilter = set() if not capacity else ScalableBloomFilter(capacity, error_rate=0.001)
        return

    def update(self, url_list):
        """
        update this urlfilter using a url_list
        """
        for url in url_list:
            self._urlfilter.add(url)
        return

    def check(self, url):
        """
        check the url based on self._re_black_list and self._re_white_list
        """
        for re_black in self._re_black_list:
            if re_black.search(url):
                return False

        for re_white in self._re_white_list:
            if re_white.search(url):
                return True

        return False if self._re_white_list else True

    def check_and_add(self, url):
        """
        check the url to make sure it hasn't been fetched, and add url to this urlfilter
        """
        result = False
        if self.check(url):
            if isinstance(self._urlfilter, set):
                result = (url not in self._urlfilter)
                self._urlfilter.add(url)
            else:
                result = (not self._urlfilter.add(url))
        return result
