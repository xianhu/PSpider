# _*_ coding: utf-8 _*_

"""
util_funcs.py by xianhu
"""

import re
import urllib.parse
from .util_config import CONFIG_URL_LEGAL_RE, CONFIG_ERROR_MESSAGE_RE

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
    check a url is legal or not, return True or False
    """
    return True if CONFIG_URL_LEGAL_RE.match(url) else False


def get_url_legal(url, base_url, encoding=None):
    """
    get a legal url from a url, based on base_url
    """
    return urllib.parse.urljoin(base_url, urllib.parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]|", encoding=encoding))


def get_url_params(url, encoding="utf-8"):
    """
    get main_part(a string) and query_part(a dictionary) from a url
    """
    frags = urllib.parse.urlparse(url, allow_fragments=True)
    components = (frags.scheme, frags.netloc, frags.path, frags.params, "", "")
    return urllib.parse.urlunparse(components), urllib.parse.parse_qs(frags.query, encoding=encoding)


def get_string_num(string, ignore_sign=False):
    """
    get a float number from a string
    """
    string_re = re.search(r"(?P<sign>-?)(?P<num>\d+(\.\d+)?)", string.replace(",", ""), flags=re.IGNORECASE)
    return float((string_re.group("sign") if not ignore_sign else "") + string_re.group("num")) if string_re else None


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


def parse_error_message(line):
    """
    parse error message based on CONFIG_ERROR_MESSAGE, return a tuple (priority, keys, deep, url)
    """
    r = CONFIG_ERROR_MESSAGE_RE.search(line)
    return int(r.group("priority")), eval(r.group("keys").strip()), int(r.group("deep")), r.group("url").strip()
