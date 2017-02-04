# _*_ coding: utf-8 _*_

"""
install script: python3 setup.py install
"""

from setuptools import setup, find_packages

setup(
    name="spider",
    version="2.0.0",
    author="xianhu",
    keywords=["spider", "crawler"],
    packages=find_packages(exclude=("otherfiles", "test", "test.*", "demos_*")),
    package_data={
        "": ["*.conf"],         # include all *.conf files
    },
    install_requires=[
        "aiohttp>=1.2.0",       # aiohttp, http for asyncio
        "pybloom_live>=2.1.0",  # pybloom-live, fork from pybloom
        "requests>=2.10.0",     # requests, http for humans
    ]
)
