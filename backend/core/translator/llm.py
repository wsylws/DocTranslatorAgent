# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base.py
# Time       ：2025/1/4 18:55
# Author     ：vince
# Description：
"""
from typing import List

from core.translator.base import BaseTranslator
from core.vo import TranslateResult


class LlmTranslator(BaseTranslator):

    async def async_translate(self, texts: List[str], source_lang: str, target_lang: str):
        from core.config import configuration
        for i, text in enumerate(texts):
            llm_result = configuration.llm.predict(messages=assemble_message(text, source_lang, target_lang))
            yield TranslateResult(index=i, result=llm_result)

    def translate(self, texts: List[str], source_lang: str, target_lang: str) -> List[TranslateResult]:
        from core.config import configuration

        result = []
        for i, text in enumerate(texts):
            llm_result = configuration.llm.predict(messages=assemble_message(text, source_lang, target_lang))
            result.append(TranslateResult(index=i, result=llm_result))
        return result

def assemble_message(text, source_lang, target_lang):
    return [
        {
            "role": "system",
            "content": "You are a leader in the academic field with rich academic experience and cross-disciplinary expertise. You not only participate in cutting-edge research, but also actively share your expertise and insights. You are also an expert in paper translation.",
        },
        {
            "role": "user",
            "content": f"Translate the following source text in {source_lang} to {target_lang}. Keep formulas, reference subscripts, and names unchanged. Output the translated content directly without any additional text. \nSource text: {text}",
        },
    ]