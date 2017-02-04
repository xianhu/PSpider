# _*_ coding: utf-8 _*_

"""
define ThreadPool as WebSpider, and AsyncPool as WebSpiderAsync
"""

from .concur_threads import ThreadPool as WebSpider
from .concur_async import AsyncPool as WebSpiderAsync
from .concur_async_insts import FetcherAsync, ParserAsync, SaverAsync
