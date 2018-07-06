# _*_ coding: utf-8 _*_

"""
install script: python3 setup.py install
"""

from setuptools import setup, find_packages

setup(
    name="spider",
    version="1.4.3",
    author="xianhu",
    keywords=["spider", "crawler", "multi-threads", "distributed", "proxies"],
    packages=find_packages(exclude=("test.*",)),
    package_data={
        "": ["*.conf"],         # include all *.conf files
    },
    install_requires=[
        "pybloom_live>=2.3.0",  # pybloom-live, fork from pybloom
        "redis>=2.10.0",        # redis, python client for redis
        "requests>=2.18.0",     # requests, http for humans
    ]
)
