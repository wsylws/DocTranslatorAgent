# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base.py
# Time       ：2025/1/1 14:34
# Author     ：vince
# Description：
"""
from abc import abstractmethod
from typing import List

from core.vo import ReaderResult


class BaseReader:

    def __init__(self, file):
        self.file = file

    @abstractmethod
    def read(self) -> List[ReaderResult]:
        pass