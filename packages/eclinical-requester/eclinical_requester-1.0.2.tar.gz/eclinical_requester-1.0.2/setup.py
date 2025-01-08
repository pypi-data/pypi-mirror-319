# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 1/8/2025 3:04 PM
@Description: Description
@File: setup.py
"""

import re

import setuptools
from setuptools import find_packages

version = ""
with open('src/api_requester/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eclinical_requester",
    version=version,
    author="xiaodong.li",
    author_email="",
    description="edetek api requester",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://example.com",
    install_requires=[
        'lxml>=5.1.0',
        'requests>=2.32.0',
        'PyYAML>=6.0.1',
        'requests-toolbelt>=1.0.0',
        'python-dateutil>=2.9.0.post0',
        'numpy>=1.26.4',
        'pycryptodome>=3.19.1',
    ],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
)
