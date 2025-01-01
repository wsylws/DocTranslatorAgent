# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base.py
# Time       ：2025/1/1 18:52
# Author     ：vince
# Description：
"""
from abc import abstractmethod


class BaseLlm:

    @abstractmethod
    def predict(self, messages):
        pass