# _*_ coding: utf-8 _*_

"""
install script: python3 setup.py install
"""

from setuptools import setup, find_packages

setup(
    name="spider",
    version="2.6.0",
    author="xianhu",
    keywords=["spider", "crawler"],
    packages=find_packages(exclude=("test.*",)),
    package_data={
        "config": ["*.conf"],  # include all *.conf files
    },
    install_requires=[]
)
