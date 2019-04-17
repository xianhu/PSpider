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
    "parse_raw_form",
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
    return urllib.parse.urljoin(base_url, urllib.parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]|", encoding=encoding))


def get_url_params(url, encoding="utf-8"):
    """
    get main_part(a string) and query_part(a dictionary) from a url
    """
    frags = urllib.parse.urlparse(url)
    components = (frags.scheme, frags.netloc, frags.path, frags.params, "", "")
    return urllib.parse.urlunparse(components), urllib.parse.parse_qs(frags.query, encoding=encoding)


def get_dict_buildin(dict_obj, _types=(int, float, bool, str, list, tuple, set, dict)):
    """
    get a dictionary from value, ignore non-buildin object
    """
    ignore = {key for key in dict_obj if not isinstance(dict_obj[key], _types)}
    return {key: dict_obj[key] for key in dict_obj if key not in ignore}


def parse_error_info(line):
    """
    parse error information based on CONFIG_***_MESSAGE, return a tuple (priority, keys, deep, url)
    """
    regu = re.search(CONFIG_MESSAGE_PATTERN, line, flags=re.IGNORECASE)
    return int(regu.group("priority")), eval(regu.group("keys").strip()), int(regu.group("deep")), regu.group("url").strip()


def parse_raw_form(raw_form_string, ignore_none=False):
    """
    parse form from a raw string, which copied from charles or fiddler
    """
    forms = {}
    for item in raw_form_string.strip().split("&"):
        frags = [i.strip() for i in item.strip().split("=")]
        assert len(frags) == 2
        if ignore_none and (not frags[1]):
            continue
        forms[frags[0]] = urllib.parse.unquote(frags[1])
    return forms


def parse_raw_request(raw_request_string, header_keys=None):
    """
    parse headers and cookies from a raw string, which copied from charles or fiddler
    """
    headers, cookies = {}, {}
    for frags in [line.strip().split(":") for line in raw_request_string.strip().split("\n") if line.strip()]:
        if frags[0].strip().lower() in CONFIG_HEADERS_SET:
            headers[frags[0].strip()] = ":".join(frags[1:]).strip()
        if header_keys and (frags[0].strip() in header_keys):
            headers[frags[0].strip()] = ":".join(frags[1:]).strip()
        if frags[0].strip().lower() == "cookie":
            cookies = {pair[0]: "=".join(pair[1:]) for pair in [cookie.strip().split("=") for cookie in ":".join(frags[1:]).strip().split(";")]}
    return headers, cookies
