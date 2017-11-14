# _*_ coding: utf-8 _*_

"""
util_fetch.py by xianhu
"""

import re
import sys
import traceback

__all__ = [
    "extract_error_info",
    "parse_error_info",
]


def extract_error_info(excep):
    """
    extract error information from exception, return a string
    """
    _type, _value, _traceback = sys.exc_info()
    tb_list = traceback.extract_tb(_traceback)
    return "filename=%s, line=%s, function=%s, error=%s" % (tb_list[-1].filename, tb_list[-1].lineno, tb_list[-1].name, excep)


def parse_error_info(line):
    """
    parse error information based on CONFIG_***_MESSAGE, return a tuple(priority, keys, deep, url)
    """
    re_search = re.search(r"priority=(?P<priority>\d+?), keys=(?P<keys>.+?), deep=(?P<deep>\d+?), (repeat=\d+, )?url=(?P<url>.+?)$", line.strip())
    priority = int(re_search.group("priority"))
    try:
        keys = eval(re_search.group("keys").strip())
    except Exception:
        keys = re_search.group("keys").strip()
    deep = int(re_search.group("deep"))
    url = re_search.group("url").strip()
    return priority, keys, deep, url
