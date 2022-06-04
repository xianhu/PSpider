# _*_ coding: utf-8 _*_

"""
util_urlfilter.py by xianhu
"""

import re


class UrlFilter(object):
    """
    class of UrlFilter, to filter urls by regexs and set
    """
    re_url_legal = re.compile(r"^https?:\S+?\.\S+?", flags=re.IGNORECASE)
    re_url_illegal = re.compile(
        r"\.(cab|iso|zip|rar|tar|gz|bz2|7z|tgz|apk|exe|app|pkg|bmg|rpm|deb|dmg|jar|jad|bin|msi|"
        "pdf|doc|docx|xls|xlsx|ppt|pptx|txt|md|odf|odt|rtf|py|java|c|cc|js|css|log|csv|tsv|"
        "jpg|jpeg|png|gif|bmp|xpm|xbm|ico|drm|dxf|eps|psd|pcd|pcx|tif|tiff|"
        "mp3|mp4|swf|mkv|avi|flv|mov|wmv|wma|3gp|mpg|mpeg|mp4a|wav|ogg|rmvb)$", flags=re.IGNORECASE
    )

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
