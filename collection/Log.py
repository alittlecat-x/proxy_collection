#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
ALi
20180822
"""

import logging
import logging.handlers

import Config


"""
写日志
"""
class Log(object):
    __log_path = Config.log_path  # 0
    __catch_log_path = Config.catch_log_path  # 1
    __redis_log_path = Config.redis_log_path  # 2
    __error_log_path = Config.error_log_path  # 3

    def __init__(self):
        self.logs = Logs([
            self.__log_path,
            self.__catch_log_path,
            self.__redis_log_path,
            self.__error_log_path])

    def catch_log(self, url, num):
        self.logs.log(0, 'INFO  ---\tCatch:%d IP(s), From:%s' % (num, url))
        self.logs.log(1, 'INFO  ---\tCatch:%d IP(s), From:%s' % (num, url))

    def catch_error_log(self, url, e):
        self.logs.log(0, 'ERROR ---\tCatch:0 IP(s), From:%s, Error:%s' % (url, e))
        self.logs.log(3, 'ERROR ---\tCatch:0 IP(s), From:%s, Error:%s' % (url, e))

    def catch_redis_log(self, num):
        self.logs.log(0, 'INFO  ---\tRedis Save:%d IP(s)' % num)
        self.logs.log(2, 'INFO  ---\tRedis Save:%d IP(s)' % num)

    def catch_redis_error_log(self, e):
        self.logs.log(0, 'ERROR  ---\tRedis Save:0 IP(s), Error:%s' % e)
        self.logs.log(3, 'ERROR  ---\tRedis Save:0 IP(s), Error:%s' % e)


"""
多日志
"""
class Logs(object):
    __log_format = '--- %(asctime)s %(message)s'
    __date_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, paths):
        self.__log = []
        for i, path in enumerate(paths):
            self.__log.append(logging.getLogger('path_%d' % i))
            log_handler = logging.handlers.RotatingFileHandler(path, 'a', 0, 1)
            log_format = logging.Formatter(self.__log_format, self.__date_format)
            log_handler.setFormatter(log_format)
            self.__log[i].addHandler(log_handler)
            self.__log[i].setLevel(logging.CRITICAL)

    def log(self, i, message):
        if i in range(len(self.__log)):
            self.__log[i].critical(message)
