# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/1/7
@Author   : shweZheng
@Software : PyCharm
"""
from setuptools import setup, find_packages

try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = 'A simple async HTTP client based on aiohttp'

setup(
    name='multifuncpy',
    version='0.1.1',
    author='shweZheng',
    author_email='shiweisai@gmail.com',
    description='A simple async HTTP client based on aiohttp',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wieszheng',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires='>=3.7',
    install_requires=[
        'aiohttp>=3.8.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',  # 添加操作系统兼容性说明
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',  # 增加3.12支持
        'Topic :: Internet :: WWW/HTTP',  # 添加主题分类
    ]
)
