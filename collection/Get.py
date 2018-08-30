#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
ALi
20180823
"""

from threading import Lock
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import time
import random

import Request
import Catch
import Save
import Log


"""
获取代理IP
get
    controls 爬取控制
    thread_num 最大线程数
    host 默认'127.0.0.1'
    port 默认6379
"""
class Get(object):
    __num = 0
    __lock = Lock()

    def get(self, controls, thread_num=100, host='127.0.0.1', port=6379):
        thread_pool = ThreadPoolExecutor(max_workers=thread_num)
        save = Save.Save(host, port)
        log = Log.Log()
        for control in controls:
            url = control['control_get']['url']['url']
            regular = control['control_get']['url']['regular']
            pages = control['control_get']['pages']
            sleep_time = control['control_get']['sleep_time']
            times = control['control_get']['times']
            timeout = control['control_get']['timeout']
            timeout_num = control['control_get']['timeout_num']
            control_catch = control['control_catch']
            catch = Catch.Catch(url, control_catch)
            for page in range(1, pages + 1):
                page_url = regular % (url, page)
                thread = thread_pool.submit(
                        self.__get,
                        catch,
                        save,
                        log,
                        page_url,
                        sleep_time,
                        times,
                        timeout,
                        timeout_num)
        thread_pool.shutdown()
        save.finish()
        log.catch_redis_log(self.__num)

    def __get(self, catch, save, log, url, sleep_time,
              times, timeout, timeout_num):
        data = []
        sleeping_time = sleep_time
        for i in range(1, times + 1):
            response = Request.Request(url, timeout, timeout_num)
            if response.result != 'Error':
                if response.status == 200:
                    data_catch = catch.catch(response.result)
                    log.catch_log(url, len(data_catch))
                    data += data_catch
                    break
                else:
                    if i < times:
                        sleeping_time = sleep_time * random.randint(1, i)
                        time.sleep(sleeping_time)
                    else:
                        log.catch_error_log(url, 'Status[%d]' % response.status)
            else:
                log.catch_error_log(url, response.e)
                break
        time.sleep(sleep_time)
        num = save.save(data)
        self.__lock.acquire()
        self.__num =self.__num + num
        self.__lock.release()


# 示例
"""
controls = [
    {
        'control_get': {
            'url': {
                'url': 'https://www.kuaidaili.com/free/inha',
                'regular': '%s/%d/'
            },
            'pages': 10,
            'sleep_time': 0.2,
            'times': 20,
            'timeout': 10,
            'timeout_num': 5
        },
        'control_catch': {
            'ip': {
                'xpath': '//*[@id="list"]/table/tbody/tr[position()>=1 and position()<=last()]/td[1]',
                'match': r'^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$',
                'replace': []
            },
            'port': {
                'xpath': '//*[@id="list"]/table/tbody/tr[position()>=1 and position()<=last()]/td[2]',
                'match': r'^([0-9]|[1-9]\d|[1-9]\d{2}|[1-9]\d{3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$',
                'replace': []
            },
            'type': {
                'xpath': '//*[@id="list"]/table/tbody/tr[position()>=1 and position()<=last()]/td[4]',
                'match': r'^(HTTP|HTTPS)$',
                'replace': []
            },
            'place': {
                'xpath': '//*[@id="list"]/table/tbody/tr[position()>=1 and position()<=last()]/td[5]',
                'match': r'',
                'replace': [[' ', '']]
            }
        }
    }
]
Get().get(controls, 10)
"""
