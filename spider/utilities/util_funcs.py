# _*_ coding: utf-8 _*_

"""
util_funcs.py by xianhu
"""

import re
import urllib.parse
from .util_config import CONFIG_URL_LEGAL_PATTERN, CONFIG_MESSAGE_PATTERN, CONFIG_HEADERS_SET

__all__ = [
    "check_url_legal",
    "get_string_num",
    "get_string_strip",
    "get_url_legal",
    "get_url_params",
    "get_dict_buildin",
    "parse_error_info",
    "parse_raw_request",
]


def check_url_legal(url):
    """
    check that a url is legal or not
    """
    return True if re.match(CONFIG_URL_LEGAL_PATTERN, url, flags=re.IGNORECASE) else False


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


def get_url_legal(url, base_url, encoding=None):
    """
    get a legal url from a url, based on base_url
    """
    legal_url = urllib.parse.urljoin(base_url, url)
    return urllib.parse.quote(legal_url, safe="%/:=&?~#+!$,;'@()*[]|", encoding=encoding)


def get_url_params(url, keep_blank_value=False, encoding="utf-8"):
    """
    get main_part(a string) and query_part(a dictionary) from a url
    """
    frags = urllib.parse.urlparse(url)
    components = (frags.scheme, frags.netloc, frags.path, frags.params, "", "")
    query_part = urllib.parse.parse_qs(frags.query, keep_blank_values=keep_blank_value, encoding=encoding)
    return urllib.parse.urlunparse(components), query_part


def get_dict_buildin(dict_obj, _type=(int, float, bool, str, list, tuple, set, dict)):
    """
    get a dictionary from value, ignore non-buildin object
    """
    non_buildin = {key for key in dict_obj if not isinstance(dict_obj[key], _type)}
    return {key: dict_obj[key] for key in dict_obj if key not in non_buildin}


def parse_error_info(line):
    """
    parse error information based on CONFIG_***_MESSAGE, return a tuple (priority, keys, deep, url)
    """
    regu = re.search(CONFIG_MESSAGE_PATTERN, line, flags=re.IGNORECASE)
    return int(regu.group("priority")), eval(regu.group("keys").strip()), int(regu.group("deep")), regu.group("url").strip()


def parse_raw_request(raw_request_string, _type="charles"):
    """
    parse headers and cookies from a raw string, which copied from charles or fiddler
    """
    headers, cookies = {}, {}
    assert _type in ("charles", "fiddler")
    for frags in [line.strip().split(":") for line in raw_request_string.strip().split("\n") if line.strip()]:
        if frags[0].strip().lower() in CONFIG_HEADERS_SET:
            headers[frags[0].strip()] = ":".join(frags[1:]).strip()
        if frags[0].strip().lower() == "Cookie":
            cookies = {pair[0].strip(): "=".join(pair[1:]).strip() for pair in ":".join(frags[1:]).strip().split("=")}
    return headers, cookies
