# _*_ coding: utf-8 _*_

"""
define WebSpider, WebSpiderDist, and also define utilities and instances for web_spider
"""

__version__ = "1.4.3"

from .utilities import *
from .instances import Fetcher, Parser, Saver, Proxieser
from .concurrent import TPEnum, WebSpider, WebSpiderDist
