# _*_ coding: utf-8 _*_

"""
util_urlfilter.py by xianhu
"""

import re
import pybloom_live
from .util_config import CONFIG_URLPATTERN_ALL


class UrlFilter(object):
    """
    class of UrlFilter, to filter url by regexs and (bloomfilter or set)
    """

    def __init__(self, black_patterns=(CONFIG_URLPATTERN_ALL,), white_patterns=("^http",), capacity=None):
        """
        constructor, use variable of BloomFilter if capacity else variable of set
        """
        self._re_black_list = [re.compile(pattern, flags=re.IGNORECASE) for pattern in black_patterns]
        self._re_white_list = [re.compile(pattern, flags=re.IGNORECASE) for pattern in white_patterns]

        self._url_set = set() if not capacity else None
        self._bloom_filter = pybloom_live.ScalableBloomFilter(capacity, error_rate=0.001) if capacity else None
        return

    def update(self, url_list):
        """
        update this urlfilter using url_list
        """
        if self._url_set is not None:
            self._url_set.update(url_list)
        else:
            for url in url_list:
                self._bloom_filter.add(url)
        return

    def check(self, url):
        """
        check the url based on self._re_black_list and self._re_white_list
        """
        # if url in black_list, return False
        for re_black in self._re_black_list:
            if re_black.search(url):
                return False

        # if not white_list, return True
        if not self._re_white_list:
            return True

        # if url in white_list, return True
        for re_white in self._re_white_list:
            if re_white.search(url):
                return True

        # return False
        return False

    def check_and_add(self, url):
        """
        check the url to make sure that the url hasn't been fetched, and add url to urlfilter
        """
        result = False
        if self.check(url):
            if self._url_set is not None:
                result = (url not in self._url_set)
                self._url_set.add(url)
            else:
                result = (not self._bloom_filter.add(url))
        return result
