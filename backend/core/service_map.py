# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : service_map.py
# Time       ：2025/1/4 18:58
# Author     ：vince
# Description：
"""
from core.models.llm.openai_llm import OpenAILlm
from core.reader.pdf import PdfTextReader, PdfOcrReader, MinerUReader
from core.translator.llm import LlmTranslator

reader_map: dict = {
    "PdfTextReader": PdfTextReader,
    "PdfOcrReader": PdfOcrReader,
    "MinerUReader": MinerUReader
}

translator_map: dict = {
    "LlmTranslator": LlmTranslator
}

llm_map: dict = {
    "OpenAILlm": OpenAILlm
}