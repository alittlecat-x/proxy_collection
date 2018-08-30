#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
ALi
20180823
"""

import Config


"""
清理日志
"""
def clean(paths):
    for path in paths:
        with open(path, 'w') as file:
            file.truncate()


paths = [Config.log_path,
    Config.catch_log_path,
    Config.redis_log_path,
    Config.error_log_path]
clean(paths)
