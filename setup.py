# _*_ coding: utf-8 _*_

"""
install script: python3 setup.py install
"""

from setuptools import setup, find_packages

setup(
    name="spider",
    version="1.0.1",
    author="xianhu",
    keywords=["spider", "crawler"],
    packages=find_packages(exclude=("test", "test.*", "demos_*")),
    package_data={
        "": ["*.conf"],         # all *.conf files
    },
    install_requires=[
        "chardet>=2.3.0",       # chardet
        "PyMySQL>=0.7.2",       # PyMySQL
        "pybloom>=2.0.0",       # pybloom, from github(https://github.com/jaybaird/python-bloomfilter)
    ]
)
