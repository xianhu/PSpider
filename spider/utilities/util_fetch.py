# _*_ coding: utf-8 _*_

"""
util_fetch.py by xianhu
"""

import re
import random
from .util_config import CONFIG_USERAGENT_PC, CONFIG_USERAGENT_PHONE, CONFIG_USERAGENT_ALL

__all__ = [
    "make_random_useragent",
    "parse_error_message",
]


def make_random_useragent(ua_type="all"):
    """
    make a random user_agent based on ua_type, ua_type can be "pc", "phone" or "all"(default)
    """
    ua_type = ua_type.lower()
    assert ua_type in ("pc", "phone", "all"), "make_random_useragent: parameter ua_type[%s] is invalid" % ua_type
    return random.choice(CONFIG_USERAGENT_PC if ua_type == "pc" else CONFIG_USERAGENT_PHONE if ua_type == "phone" else CONFIG_USERAGENT_ALL)


def parse_error_message(line):
    """
    parse error message based on CONFIG_***_MESSAGE
    :return (priority, keys, deep, url): a tuple, used in set_start_url
    """
    line_no_repeat = re.sub(r"repeat=\d+, ", "", line.strip())
    re_search = re.search(r"priority=(?P<priority>\d+?), keys=(?P<keys>.+?), deep=(?P<deep>\d+?), url=(?P<url>.+?)$", line_no_repeat)
    priority = int(re_search.group("priority"))
    try:
        keys = eval(re_search.group("keys").strip())
    except Exception:
        keys = re_search.group("keys").strip()
    deep = int(re_search.group("deep"))
    url = re_search.group("url").strip()
    return priority, keys, deep, url
