# _*_ coding: utf-8 _*_

"""
define ThreadPool as WebSpider, and DistThreadPool as WebSpiderDist
"""

from .concur_threads import ThreadPool as WebSpider
from .distributed_threads import DistThreadPool as WebSpiderDist
