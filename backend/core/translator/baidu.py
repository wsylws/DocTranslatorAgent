# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : baidu.py
# Time       ：2025/1/7 23:21
# Author     ：vince
# Description：
"""
from typing import List

from core.translator.base import BaseTranslator
from core.vo import TranslateResult
import requests
import random
from hashlib import md5


class BaiduTranslator(BaseTranslator):

    def translate(self, texts: List[str], source_lang: str, target_lang: str) -> List[TranslateResult]:
        for i, text in enumerate(texts):
            translate_result = BaiduTranslator.baidu_translate(text, source_lang, target_lang)
            yield TranslateResult(index=i, result=translate_result)

    async def async_translate(self, texts: List[str], source_lang: str, target_lang: str) -> List[TranslateResult]:
        result = []
        for i, text in enumerate(texts):
            translate_result = BaiduTranslator.baidu_translate(text, source_lang, target_lang)
            result.append(TranslateResult(index=i, result=translate_result))
        return result

    @staticmethod
    def baidu_translate(text, source_lang, target_lang):
        from core.config import configuration

        appid = configuration.baidu['appid']
        appkey = configuration.baidu['appkey']

        # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
        from_lang = source_lang
        to_lang = target_lang

        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        url = endpoint + path

        query = text

        # Generate salt and sign
        def make_md5(s, encoding='utf-8'):
            return md5(s.encode(encoding)).hexdigest()

        salt = random.randint(32768, 65536)
        sign = make_md5(appid + query + str(salt) + appkey)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()
        return result['trans_result'][0]['dst']