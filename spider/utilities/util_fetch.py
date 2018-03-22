# _*_ coding: utf-8 _*_

"""
util_fetch.py by xianhu
"""

import re

__all__ = [
    "parse_error_info",
]


def parse_error_info(line):
    """
    parse error information based on CONFIG_***_MESSAGE, return a tuple (priority, keys, deep, url)
    """
    regu = re.search(r"priority=(?P<priority>\d+?),\s*?keys=(?P<keys>.+?),\s*?deep=(?P<deep>\d+?),\s*?(repeat=\d+,)?\s*?url=(?P<url>.+?)$", line)
    return int(regu.group("priority")), eval(regu.group("keys").strip()), int(regu.group("deep")), regu.group("url").strip()
