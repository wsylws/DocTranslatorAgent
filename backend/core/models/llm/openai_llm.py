# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : openai_llm.py
# Time       ：2025/1/1 18:49
# Author     ：vince
# Description：
"""
from time import sleep

import openai

from core.models.llm.base import BaseLlm


class OpenAILlm(BaseLlm):

    def __init__(
        self,
        model,
        base_url=None,
        api_key=None,
        temperature=0.1
    ):
        self.temperature = temperature
        self.client = openai.OpenAI(
            base_url=base_url or self.envs["OPENAI_BASE_URL"],
            api_key=api_key or self.envs["OPENAI_API_KEY"],
        )
        self.model = model

    def predict(self, messages):
        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=messages
        )
        return ''.join([choice.message.content for choice in completion.choices])
