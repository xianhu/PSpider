# _*_ coding: utf-8 _*_

"""
util_fetch.py by xianhu
"""

import time
import random
import urllib.parse
import urllib.request
import http.cookiejar
from .util_config import CONFIG_HEADERS_MAP, CONFIG_USERAGENT_PC, CONFIG_USERAGENT_PHONE, CONFIG_USERAGENT_ALL

__all__ = [
    "make_cookie",
    "make_cookies_maps",
    "make_cookies_string",
    "make_cookiejar_opener",
    "make_headers",
    "make_post_data",
    "make_referer_url",
]


def make_cookie(name, value, domain, port=None, path=None, expires=None):
    """
    make cookie based on "name", "value" and "domain", etc. domain must like ".baidu.com" or "baidu.com"
    :key: cookiejar.set_cookie(cookie)
    """
    # check parameters
    assert (not domain.startswith("http")) and (not domain.startswith("www.")), "make_cookie: domain is invalid"

    # change parameters
    path = "/" if not path else path
    expires = (time.time() + 3600 * 24 * 30) if not expires else expires

    # make cookie
    cookie = http.cookiejar.Cookie(
        version=0, name=name, value=value, port=port, port_specified=False,
        domain=domain, domain_specified=False, domain_initial_dot=False, path=path, path_specified=True,
        secure=False, expires=expires, discard=True, comment=None, comment_url=None, rest=None
    )
    return cookie


def make_cookies_maps(cookies_maps):
    """
    make cookies list from a map_list, cookies_maps: [{"name": xxx, "value": xxx, "domain": xxx, ...}, ...]
    :key: for cookie in cookies_list: cookiejar.set_cookie(cookie)
    """
    cookies_list = [
        make_cookie(item["name"], item["value"], item["domain"], port=item.get("port"), path=item.get("path"), expires=item.get("expires"))
        for item in cookies_maps if ("name" in item) and ("value" in item) and ("domain" in item)
    ]
    return cookies_list


def make_cookies_string(cookies_string, domain):
    """
    make cookies list from a string, cookies_string: "name1=value1; name2=value2", this string also can be one part of headers
    :key: for cookie in cookies_list: cookiejar.set_cookie(cookie)
    """
    frags = [item.strip() for item in cookies_string.strip("; ").split(";") if item.strip()]
    cookies_list = [make_cookie(k.strip(), v.strip(), domain) for k, v in [item.split("=") for item in frags] if k.strip()]
    return cookies_list


def make_cookiejar_opener(is_cookie=True, proxies=None):
    """
    make cookiejar and opener for requesting, proxies: None or {"http": "http://proxy.example.com:8080/"}
    :key: opener.addheaders = make_headers(...).items()
    """
    assert is_cookie or proxies, "make_cookiejar_opener: one of parameters(is_cookie, proxies) must be True"
    cookie_jar, opener = None, None
    if is_cookie:
        cookie_jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar=cookie_jar))
    if proxies:
        if opener:
            opener.add_handler(urllib.request.ProxyHandler(proxies=proxies))
        else:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies=proxies))
    return cookie_jar, opener


def make_headers(user_agent="pc", **kwargs):
    """
    make dictionary headers for requesting, user_agent: "pc", "phone", "all" or a ua_string
    :key: headers["Cookie"] = cookies_string
    """
    kwargs["user_agent"] = random.choice(CONFIG_USERAGENT_ALL) if user_agent == "all" else (
        random.choice(CONFIG_USERAGENT_PC) if user_agent == "pc" else (
            random.choice(CONFIG_USERAGENT_PHONE) if user_agent == "phone" else user_agent
        )
    )
    return {CONFIG_HEADERS_MAP[key]: kwargs[key] for key in kwargs if key in CONFIG_HEADERS_MAP}


def make_post_data(post_dict, boundary=None):
    """
    make post_data based on post_dict, post_dict: {name: value, ...}
    :key: "Content-Type" in headers is "multipart/form-data; boundary=----WebKitFormBoundaryzUJDUghs3ChlA3U1"
    :param post_dict: if include file, name must start with "_file_", and value=[file_bytes, file_name, con_name, con_type]
    """
    # make post_data without boundary and file
    if not boundary:
        return urllib.parse.urlencode(post_dict).encode()

    # make post_data with boundary and file
    post_data = []
    for name, value in post_dict.items():
        if name.startswith("_file_"):
            file_bytes, file_name, con_name, con_type = value
            post_data.append(("--%s" % boundary).encode())
            post_data.append(('Content-Disposition: form-data; name="%s"; filename="%s"' % (con_name, file_name)).encode())
            post_data.append(("Content-Type: %s\r\n" % con_type).encode())
            post_data.append(file_bytes)
        else:
            post_data.append(("--%s" % boundary).encode())
            post_data.append(('Content-Disposition: form-data; name="%s"\r\n' % name).encode())
            post_data.append(str(value).encode())
    post_data.append(("--%s--\r\n" % boundary).encode())
    return b'\r\n'.join(post_data)


def make_referer_url(url, path=False):
    """
    make referer url for requesting, set params = "", query = "" and fragment = ""
    :param path: default False, whether referer_url include path
    """
    url_frags = urllib.parse.urlparse(url, allow_fragments=True)
    url_path = url_frags.path if path else "/"
    return urllib.parse.urlunparse((url_frags.scheme, url_frags.netloc, url_path, "", "", ""))
