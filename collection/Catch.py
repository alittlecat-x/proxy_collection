#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
ALi
20180817
"""

import re
import time

from lxml import etree


"""
对爬取结果进行解析
初始化参数
    url 爬取地址
    control 匹配规则
catch
    response 爬取的页面
"""
class Catch(object):
    def __init__(self, url, control):
        self.__url = url
        self.__ip_xpath = control['ip']['xpath']
        self.__ip_match = control['ip']['match']
        self.__ip_replace = control['ip']['replace']
        self.__port_xpath = control['port']['xpath']
        self.__port_match = control['port']['match']
        self.__port_replace = control['port']['replace']
        self.__type_xpath = control['type']['xpath']
        self.__type_match = control['type']['match']
        self.__type_replace = control['type']['replace']
        self.__place_xpath = control['place']['xpath']
        self.__place_match = control['place']['match']
        self.__place_replace = control['place']['replace']

    def catch(self, response):
        html = etree.HTML(response)
        data = []
        try:
            if self.__ip_xpath != '' and self.__port_xpath != '':
                ip = html.xpath(self.__ip_xpath)
                if len(self.__ip_replace) != 0:
                    for f, r in self.__ip_replace:
                        for i in range(len(ip)):
                            ip[i].text = ip[i].text.replace(f, r)
                port = html.xpath(self.__port_xpath)
                if len(self.__port_replace) != 0:
                    for f, r in self.__port_replace:
                        for i in range(len(port)):
                            port[i].text = port[i].text.replace(f, r)
                if self.__type_xpath == '':
                    type = ['HTTP'] * len(ip)
                else:
                    type = html.xpath(self.__type_xpath)
                    if len(self.__type_replace) != 0:
                        for f, r in self.__type_replace:
                            for i in range(len(type)):
                                type[i].text = type[i].text.replace(f, r)
                if self.__place_xpath == '':
                    place = [''] * len(ip)
                else:
                    place = html.xpath(self.__place_xpath)
                    if len(self.__place_replace) != 0:
                        for f, r in self.__place_replace:
                            for i in range(len(place)):
                                place[i].text = place[i].text.replace(f, r)
                if len(ip) == len(port) == len(type) == len(place):
                    for i in range(len(ip)):
                        if re.match(self.__ip_match, ip[i].text) and re.match(self.__port_match, port[i].text) and re.match(
                                self.__type_match, type[i].text) and len(place[i].text) <= 1024:
                            data.append({'ip': ip[i].text,
                                         'port': port[i].text,
                                         'type': type[i].text,
                                         'place': place[i].text,
                                         'time': time.strftime('%Y-%m-%d %H:%M:%S'),
                                         'site': self.__url})
        except Exception as e:
            print(e)
        finally:
            return data
