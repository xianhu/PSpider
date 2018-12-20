# _*_ coding: utf-8 _*_

"""
define thread instances of url_fetch, htm_parse, item_save and proxies for threads_pool
"""

from .base import TPEnum, MonitorThread
from .fetch import FetchThread
from .parse import ParseThread
from .save import SaveThread
from .proxies import ProxiesThread
