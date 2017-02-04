# _*_ coding: utf-8 _*_

"""
util_parse.py by xianhu
"""

import re
import operator
import functools
import urllib.parse

__all__ = [
    "get_string_num",
    "get_string_split",
    "get_string_strip",
    "get_url_legal",
    "get_url_params",
]


def get_string_num(string, base=None):
    """
    get float number from a string, if base isn't None, K means (base * B), M means (base * K), ...
    """
    temp = re.search(r"(?P<num>\d+(\.\d+)?)(?P<param>[\w\W]*?)$", string.upper().strip(), flags=re.IGNORECASE)
    if not temp:
        return 0.0
    num, param = float(temp.group("num")), temp.group("param")
    if param.find("亿") >= 0:
        num *= 100000000
    if param.find("万") >= 0:
        num *= 10000
    if param.find("千") >= 0:
        num *= 1000
    if param.find("百") >= 0:
        num *= 100
    if param.find("十") >= 0:
        num *= 10
    if param.find("%") >= 0:
        num /= 100
    if base:
        if param.find("K") >= 0:
            num *= base
        if param.find("M") >= 0:
            num *= (base * base)
        if param.find("G") >= 0:
            num *= (base * base * base)
        if param.find("T") >= 0:
            num *= (base * base * base * base)
    return num


def get_string_split(string, split_chars=(" ", "\t", ","), is_remove_empty=False):
    """
    get string list by splitting string based on split_chars, len(split_chars) must >= 2
    """
    assert len(split_chars) >= 2, "get_string_split: parameter split_chars[%s] is invalid, the length of it must >= 2" % split_chars
    string_list = string.split(split_chars[0])
    for char in split_chars[1:]:
        string_list = functools.reduce(operator.add, [item.split(char) for item in string_list], [])
    return string_list if not is_remove_empty else [item.strip() for item in string_list if item.strip()]


def get_string_strip(string):
    """
    get string striped \t, \r, \n from a string, also change None to ""
    """
    return re.sub(r"\s+", " ", string, flags=re.IGNORECASE).strip() if string else ""


def get_url_legal(url, base_url, encoding=None):
    """
    get legal url from a url, based on base_url, and set url_frags.fragment = ""
    :key: http://stats.nba.com/player/#!/201566/?p=russell-westbrook
    """
    url_join = urllib.parse.urljoin(base_url, url, allow_fragments=True)
    url_legal = urllib.parse.quote(url_join, safe="%/:=&?~#+!$,;'@()*[]|", encoding=encoding)
    url_frags = urllib.parse.urlparse(url_legal, allow_fragments=True)
    return urllib.parse.urlunparse((url_frags.scheme, url_frags.netloc, url_frags.path, url_frags.params, url_frags.query, ""))


def get_url_params(url, is_unique_value=True, keep_blank_value=False, encoding="utf-8"):
    """
    get main_part(a string) and query_part(a dictionary) from a url
    """
    url_frags = urllib.parse.urlparse(url, allow_fragments=True)
    querys = urllib.parse.parse_qs(url_frags.query, keep_blank_values=keep_blank_value, encoding=encoding)
    main_part = urllib.parse.urlunparse((url_frags.scheme, url_frags.netloc, url_frags.path, url_frags.params, "", ""))
    query_part = {key: querys[key][0] for key in querys} if is_unique_value else querys
    return main_part, query_part
