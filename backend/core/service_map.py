# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : service_map.py
# Time       ：2025/1/4 18:58
# Author     ：vince
# Description：
"""
from core.models.llm.openai_llm import OpenAILlm
from core.reader.pdf import PdfDefaultTextReader, PdfDefaultOcrReader, MinerUTextReader, MinerUOcrReader
from core.translator.baidu import BaiduTranslator
from core.translator.llm import LlmTranslator

reader_map: dict = {
    "PdfDefaultTextReader": PdfDefaultTextReader,
    "PdfDefaultOcrReader": PdfDefaultOcrReader,
    "MinerUTextReader": MinerUTextReader,
    "MinerUOcrReader": MinerUOcrReader
}

translator_map: dict = {
    "LlmTranslator": LlmTranslator,
    "BaiduTranslator": BaiduTranslator
}

llm_map: dict = {
    "OpenAILlm": OpenAILlm
}