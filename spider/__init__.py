# _*_ coding: utf-8 _*_

"""
define WebSpider, WebSpiderAsync, and also define utilities and instances for web_spider
"""

from .utilities import *
from .instances import *
from .concurrent import WebSpider, WebSpiderAsync
from .concurrent import FetcherAsync, ParserAsync, SaverAsync
