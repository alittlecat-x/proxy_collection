#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
ALi
20180817
"""

import requests
from fake_useragent import UserAgent


"""
爬取
    url 爬取地址
    timeout 超时时间
    timeout_num 超时最大尝试次数
"""
class Request(object):
    def __init__(self, url, timeout, timeout_num):
        self.__num = 0
        response = self.__request(url, timeout)
        self.result = self.__exception(url, timeout, timeout_num, response)

    def __request(self, url, timeout):
        self.__num += 1
        try:
            headers = {'User-Agent': UserAgent().random}
            response = requests.get(url, headers=headers, timeout=timeout)
            self.status = response.status_code
            response = response.text
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
            self.e = e
            response = 'Timeout'
        except Exception as e:
            self.e = e
            response = 'Error'
        finally:
            return response

    def __exception(self, url, timeout, timeout_num, response):
        while self.__num < timeout_num:
            if response == 'Timeout':
                response = self.__request(url, timeout)
            elif response == 'Error':
                result = 'Error'
                break
            else:
                result = response
                break
            if response == 'Timeout':
                result = 'Error'
        return result
