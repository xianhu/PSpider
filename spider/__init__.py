# _*_ coding: utf-8 _*_

"""
define WebSpider, WebSpiderDist, and also define utilities and instances for web_spider
"""

__version__ = "spider-2.9.0"

from .utilities import *
from .instances import Fetcher, Parser, Saver, Proxieser
from .concurrent import TPEnum, WebSpider, WebSpiderDist
