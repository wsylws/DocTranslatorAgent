# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : config.py
# Time       ：2025/1/1 21:19
# Author     ：vince
# Description：
"""
import toml

from core.service_map import llm_map


class Configuration:

    def __init__(self):
        with open('../config.toml', 'r') as file:
            config_data = toml.load(file)
            activate_llm_name = config_data['llm']['activate_llm']
            config = config_data['llm']['llm_config']
            self.llm = llm_map.get(activate_llm_name)(**config_data[config])

configuration = Configuration()