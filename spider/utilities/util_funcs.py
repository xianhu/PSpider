# _*_ coding: utf-8 _*_

"""
util_funcs.py by xianhu
"""

import re
import urllib.parse
from .util_config import CONFIG_RE_URL_LEGAL, CONFIG_RE_ERROR_MESSAGE

__all__ = [
    "check_url_legal",
    "get_url_legal",
    "get_url_params",
    "get_string_num",
    "get_string_strip",
    "get_dict_buildin",
    "parse_error_message",
]


def check_url_legal(url):
    """
    check an url is legal or not, return True or False
    """
    return True if CONFIG_RE_URL_LEGAL.match(url) else False


def get_url_legal(url, base_url, encoding=None):
    """
    get a legal url from a url string, based on base_url
    """
    return urllib.parse.urljoin(base_url, urllib.parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]|", encoding=encoding))


def get_url_params(url, encoding="utf-8"):
    """
    get the main_part and query_part from an url
    """
    frags = urllib.parse.urlparse(url, allow_fragments=True)
    components = (frags.scheme, frags.netloc, frags.path, frags.params, "", "")
    return urllib.parse.urlunparse(components), urllib.parse.parse_qs(frags.query, encoding=encoding)


def get_string_num(string, ignore_sign=False):
    """
    get a float number from a string
    """
    reg = re.search(r"(?P<sign>-?)(?P<num>\d+(\.\d+)?)", string.replace(",", ""), flags=re.IGNORECASE)
    return float((reg.group("sign") if not ignore_sign else "") + reg.group("num")) if reg else None


def get_string_strip(string, replace_char=" "):
    """
    get a string which striped \t, \r, \n from a string, also change None to ""
    """
    return re.sub(r"\s+", replace_char, string, flags=re.IGNORECASE).strip() if string else ""


def get_dict_buildin(dict_obj, _types=(int, float, bool, str, list, tuple, set, dict)):
    """
    get a dictionary from value, ignore non-buildin object
    """
    return {key: dict_obj[key] for key in dict_obj if isinstance(dict_obj[key], _types)}


def parse_error_message(error_message):
    """
    parse error message, and return a tuple (priority, keys, deep, url)
    """
    reg = CONFIG_RE_ERROR_MESSAGE.search(error_message)
    return int(reg.group("p")), eval(reg.group("k")), int(reg.group("d")), reg.group("u").strip()
