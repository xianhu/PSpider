# _*_ coding: utf-8 _*_

"""
util_urlfilter.py by xianhu
"""

import re
import pybloom
from .util_config import CONFIG_URLPATTERN_ALL


class UrlFilter(object):
    """
    class of UrlFilter, to filter url by regexs and (bloomfilter or set)
    """

    def __init__(self, black_patterns=(CONFIG_URLPATTERN_ALL,), white_patterns=("^http",), capacity=None):
        """
        constructor, use variable of BloomFilter if capacity else variable of set
        """
        self.re_black_list = [re.compile(_pattern, flags=re.IGNORECASE) for _pattern in black_patterns]
        self.re_white_list = [re.compile(_pattern, flags=re.IGNORECASE) for _pattern in white_patterns]

        self.url_set = set() if not capacity else None
        self.bloom_filter = pybloom.ScalableBloomFilter(capacity, error_rate=0.001) if capacity else None
        return

    def update(self):
        """
        update this urlfilter, you can rewrite this function if necessary
        """
        raise NotImplementedError

    def check(self, url):
        """
        check the url to make sure that the url hasn't been fetched
        """
        # regex filter: black pattern, if match one return False
        for re_black in self.re_black_list:
            if re_black.search(url):
                return False

        # regex filter: while pattern, if miss all return False
        result = False
        for re_white in self.re_white_list:
            if re_white.search(url):
                if self.url_set is not None:
                    result = False if url in self.url_set else True
                    self.url_set.add(url)
                elif self.bloom_filter is not None:
                    # bloom filter, "add": if key already exists, return True, else return False
                    result = (not self.bloom_filter.add(url))
                else:
                    pass
                break

        # return result
        return result
