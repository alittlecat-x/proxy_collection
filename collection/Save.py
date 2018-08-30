#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
ALi
20180822
"""

import sys
import json

import redis

import Log


"""
存储到Redis
初始化参数
    host 默认'127.0.0.1'
    port 默认6379
    初始化失败程序退出
save 存数据库
finish 持久化存储
"""
class Save(object):
    def __init__(self, host='127.0.0.1', port=6379):
        try:
            self.__redis_connect = redis.ConnectionPool(host=host, port=port)
        except Exception as e:
            Log.Log().catch_redis_error_log(e)
            sys.exit(0)

    def save(self, data):
        num = 0
        for data_row in data:
            key = data_row.pop('ip')
            value = json.dumps(data_row)
            r = redis.Redis(connection_pool=self.__redis_connect)
            if r.set(key, value, nx=True):
                num += 1
        return num

    def finish(self):
        r = redis.Redis(connection_pool=self.__redis_connect)
        r.save()
