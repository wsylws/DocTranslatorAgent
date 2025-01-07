# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : mineru_ocr_reader_test.py
# Time       ：2025/1/1 15:48
# Author     ：vince
# Description：
"""
from core.reader.pdf import MinerUReader

if __name__ == '__main__':
    file_path = 'attention is all you need.pdf'
    with open(file_path, 'rb') as file:
        res = MinerUReader(file).read()
        print(res)