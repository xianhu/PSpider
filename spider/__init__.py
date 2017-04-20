# _*_ coding: utf-8 _*_

"""
define WebSpider, WebSpiderAsync, WebSpiderDist, and also define utilities and instances for web_spider
"""

from .utilities import *
from .insts_thread import Fetcher, Parser, Saver
from .insts_async import FetcherAsync, ParserAsync, SaverAsync
from .concurrent import WebSpider, WebSpiderAsync, WebSpiderDist
