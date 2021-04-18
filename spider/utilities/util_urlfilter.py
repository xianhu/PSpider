# _*_ coding: utf-8 _*_

"""
util_urlfilter.py by xianhu
"""

from .util_config import CONFIG_URL_LEGAL_RE, CONFIG_URL_ILLEGAL_RE


class UrlFilter(object):
    """
    class of UrlFilter, to filter url by regexs and set
    """

    def __init__(self, black_patterns=(CONFIG_URL_ILLEGAL_RE,), white_patterns=(CONFIG_URL_LEGAL_RE,)):
        """
        constructor
        """
        self._urlfilter = set()
        self._re_black_list = black_patterns
        self._re_white_list = white_patterns
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
        check whether url is in this urlfilter, and add url to it
        """
        result = False
        if self.check(url):
            result = (url not in self._urlfilter)
            self._urlfilter.add(url)
        return result
