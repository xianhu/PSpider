# _*_ coding: utf-8 _*_

"""
util_fetch.py by xianhu
"""

import re
import sys
import random
import traceback
from .util_config import CONFIG_USERAGENT_PC, CONFIG_USERAGENT_PHONE, CONFIG_USERAGENT_ALL

__all__ = [
    "make_random_useragent",
    "extract_error_info",
    "parse_error_info",
]


def make_random_useragent(ua_type="all"):
    """
    make a random user_agent based on ua_type, ua_type can be "pc", "phone" or "all"(default)
    """
    ua_type = ua_type.lower()
    assert ua_type in ("pc", "phone", "all"), "make_random_useragent: parameter ua_type[%s] is invalid" % ua_type
    return random.choice(CONFIG_USERAGENT_PC if ua_type == "pc" else CONFIG_USERAGENT_PHONE if ua_type == "phone" else CONFIG_USERAGENT_ALL)


def extract_error_info(excep):
    """
    extract error information from exception, return a string
    """
    info = sys.exc_info()
    tb_instance = traceback.extract_tb(info[2])
    file_name, line_number, function_name, text = tb_instance[-1]
    return "filename=%s, line=%s, function=%s, error=%s" % (file_name, line_number, function_name, excep)


def parse_error_info(line):
    """
    parse error information based on CONFIG_***_MESSAGE, return a tuple(priority, keys, deep, url)
    """
    re_search = re.search(r"priority=(?P<priority>\d+?), keys=(?P<keys>.+?), deep=(?P<deep>\d+?), (repeat=\d+, )?url=(?P<url>.+?)$", line.strip())
    priority = int(re_search.group("priority"))
    try:
        keys = eval(re_search.group("keys").strip())
    except Exception as excep:
        keys = re_search.group("keys").strip()
    deep = int(re_search.group("deep"))
    url = re_search.group("url").strip()
    return priority, keys, deep, url
