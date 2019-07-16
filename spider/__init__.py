# _*_ coding: utf-8 _*_

"""
define WebSpider, and also define utilities and instances for web_spider
"""

__version__ = "2.4.1"

from .utilities import *
from .concurrent import TPEnum, WebSpider
from .instances import Fetcher, Parser, Saver, Proxieser
