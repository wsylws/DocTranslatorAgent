# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base.py
# Time       ：2025/1/1 15:04
# Author     ：vince
# Description：
"""
from abc import abstractmethod
from typing import List

from core.vo import TextBlock


class Layout:

    @abstractmethod
    def split_blocks(self, pix) -> List[TextBlock]:
        pass