# _*_ coding: utf-8 _*_

"""
install script: python3 setup.py install
"""

from setuptools import setup, find_packages

setup(
    name="spider",
    version="1.6.4",
    author="xianhu",
    keywords=["spider", "crawler", "multi-threads", "multi-processes", "proxies"],
    packages=find_packages(exclude=("test.*",)),
    package_data={
        "": ["*.conf"],         # include all *.conf files
    },
    install_requires=[
        "pybloom_live>=3.0.0",  # pybloom-live, fork from pybloom
        "requests>=2.20.0",     # requests, http for humans
    ]
)
