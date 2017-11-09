# _*_ coding: utf-8 _*_

"""
define WebSpider, WebSpiderDist, and also define utilities and instances for web_spider
"""

__version__ = "2.8.0"

from .utilities import *
from .instances import Fetcher, Parser, Saver
from .concurrent import TPEnum, WebSpider, WebSpiderDist
