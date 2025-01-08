# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Version  : Python 3.12
@Time     : 2025/1/7
@Author   : shweZheng
@Software : PyCharm
"""
import unittest
import asyncio

from src.asynchttp import AsyncHttpClient


class TestAsyncHttpClient(unittest.TestCase):
    def setUp(self):
        self.client = AsyncHttpClient()

    def tearDown(self):
        asyncio.run(self.client.close())

    def test_get(self):
        async def get_test():
            result = await self.client.get('http://www.baidu.com/')
            self.assertIn('<title>百度一下，你就知道</title>', await result.text())

        asyncio.run(get_test())

if __name__ == '__main__':
    unittest.main()