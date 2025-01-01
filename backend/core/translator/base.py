# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base.py
# Time       ：2025/1/4 17:17
# Author     ：vince
# Description：
"""
from abc import abstractmethod
from typing import List

from core.vo import TranslateResult


class BaseTranslator:

    @abstractmethod
    def translate(self,
                  texts: List[str],
                  source_lang: str,
                  target_lang: str) -> List[TranslateResult]:
        pass

    @abstractmethod
    async def async_translate(self,
                              texts: List[str],
                              source_lang: str,
                              target_lang: str) -> List[TranslateResult]:
        pass