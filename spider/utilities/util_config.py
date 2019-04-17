# _*_ coding: utf-8 _*_

"""
util_config.py by xianhu
"""

__all__ = [
    "CONFIG_FETCH_MESSAGE",
    "CONFIG_PARSE_MESSAGE",
    "CONFIG_MESSAGE_PATTERN",
    "CONFIG_URL_LEGAL_PATTERN",
    "CONFIG_URL_ILLEGAL_PATTERN",
    "CONFIG_HEADERS_SET",
]

# define the structure of message, used in Fetcher and Parser
CONFIG_FETCH_MESSAGE = "priority=%s, keys=%s, deep=%s, repeat=%s, url=%s"
CONFIG_PARSE_MESSAGE = "priority=%s, keys=%s, deep=%s, url=%s"
CONFIG_MESSAGE_PATTERN = r"priority=(?P<priority>\d+),\s*keys=(?P<keys>.+?),\s*deep=(?P<deep>\d+),\s*(repeat=(?P<repeat>\d+),\s*)?url=(?P<url>.+)$"

# define url_legal_pattern and url_illegal_pattern
CONFIG_URL_LEGAL_PATTERN = r"^https?:[^\s]+?\.[^\s]+?"
CONFIG_URL_ILLEGAL_PATTERN = r"\.(cab|iso|zip|rar|tar|gz|bz2|7z|tgz|apk|exe|app|pkg|bmg|rpm|deb|dmg|jar|jad|bin|msi|" \
                             "pdf|doc|docx|xls|xlsx|ppt|pptx|txt|md|odf|odt|rtf|py|java|c|cc|js|css|log|csv|tsv|" \
                             "jpg|jpeg|png|gif|bmp|xpm|xbm|ico|drm|dxf|eps|psd|pcd|pcx|tif|tiff|" \
                             "mp3|mp4|swf|mkv|avi|flv|mov|wmv|wma|3gp|mpg|mpeg|mp4a|wav|ogg|rmvb)$"

# define key set of headers
CONFIG_HEADERS_SET = {item.lower() for item in {
    "Host", "Origin", "Referer", "Connection", "Etag", "Pragma", "User-Agent", "Cache-Control", "Content-Type",
    "Accept", "Accept-Encoding", "Accept-Charset", "Accept-Language", "If-Modified-Since", "If-None-Match", "Last-Modified", "Upgrade-Insecure-Requests"
}}
