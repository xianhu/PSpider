# _*_ coding: utf-8 _*_

"""
cfilter.py by xianhu
"""


class UrlFilter(object):
    """
    class of UrlFilter, to filter urls by regexs and set
    """

    def __init__(self, black_patterns=tuple(), white_patterns=tuple()):
        """
        constructor
        """
        self._url_set = set()
        self._re_black_list = black_patterns
        self._re_white_list = white_patterns
        return

    def check(self, url):
        """
        check the url based on re_black_list and re_white_list
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
        check whether url is in set, and add url to it
        """
        result = False
        if self.check(url):
            result = (url not in self._url_set)
            self._url_set.add(url)
        return result
