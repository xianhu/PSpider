# _*_ coding: utf-8 _*_

"""
define ThreadPool as WebSpider, and DistThreadPool as WebSpiderDist
"""

from .threads_inst import TPEnum
from .threads_pool import ThreadPool as WebSpider
from .threads_pool_dist import DistThreadPool as WebSpiderDist
