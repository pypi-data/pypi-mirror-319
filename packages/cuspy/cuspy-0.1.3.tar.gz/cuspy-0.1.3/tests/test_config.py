#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/5 18:22
# @Author  : zbc@mail.ustc.edu.cn
# @File    : test_config.py
# @Software: PyCharm


if __name__ == "__main__":
    from cuspy.config_utils import ConfigUtils
    config = ConfigUtils.load_config('./config.json')
    print(config)
