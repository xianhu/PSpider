# _*_ coding: utf-8 _*_

"""
util_funcs.py by xianhu
"""

import re
import urllib.parse
from .util_config import CONFIG_URL_LEGAL_PATTERN

__all__ = [
    "parse_error_info",
    "get_string_num",
    "get_string_strip",
    "get_url_params",
    "get_url_legal",
    "check_url_legal",
]


def parse_error_info(line):
    """
    parse error information based on CONFIG_***_MESSAGE, return a tuple (priority, keys, deep, url)
    """
    regu = re.search(r"priority=(?P<priority>\d+?),\s*?keys=(?P<keys>.+?),\s*?deep=(?P<deep>\d+?),\s*?(repeat=\d+,)?\s*?url=(?P<url>.+?)$", line)
    return int(regu.group("priority")), eval(regu.group("keys").strip()), int(regu.group("deep")), regu.group("url").strip()


def get_string_num(string, ignore_sign=False):
    """
    get a float number from a string
    """
    string_re = re.search(r"(?P<sign>-?)(?P<num>\d+(\.\d+)?)", get_string_strip(string.replace(",", ""), replace_char=""), flags=re.IGNORECASE)
    return float((string_re.group("sign") if not ignore_sign else "") + string_re.group("num")) if string_re else None


def get_string_strip(string, replace_char=" "):
    """
    get a string which striped \t, \r, \n from a string, also change None to ""
    """
    return re.sub(r"\s+", replace_char, string, flags=re.IGNORECASE).strip() if string else ""


def get_url_params(url, keep_blank_value=False, encoding="utf-8"):
    """
    get main_part(a string) and query_part(a dictionary) from a url
    """
    frags = urllib.parse.urlparse(url, allow_fragments=True)
    main_part = urllib.parse.urlunparse((frags.scheme, frags.netloc, frags.path, frags.params, "", ""))
    query_part = urllib.parse.parse_qs(frags.query, keep_blank_values=keep_blank_value, encoding=encoding)
    return main_part, query_part


def get_url_legal(url, base_url, encoding=None):
    """
    get a legal url from a url, based on base_url
    """
    url_join = urllib.parse.urljoin(base_url, url, allow_fragments=True)
    return urllib.parse.quote(url_join, safe="%/:=&?~#+!$,;'@()*[]|", encoding=encoding)


def check_url_legal(url):
    """
    check whether a url is legal
    """
    return True if re.match(CONFIG_URL_LEGAL_PATTERN, url, flags=re.IGNORECASE) else False
