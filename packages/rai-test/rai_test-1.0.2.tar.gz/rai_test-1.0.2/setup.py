# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

setup(
    name="rai_test",
    version="1.0.2",
    description="Alibaba Cloud PAI-RAM SAM SDK Library for Python",
    author="cedar.wxs",
    author_email="sdk-team@alibabacloud.com",
    license="Apache License 2.0",
#    url = 'https://github.com/aliyun/alibabacloud-python-sdk',
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[],
    python_requires=">=3.6",
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Topic :: Software Development"
    )
)
