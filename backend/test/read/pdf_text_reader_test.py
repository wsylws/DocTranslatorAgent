# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : pdf_text_reader_test.py
# Time       ：2025/1/1 14:41
# Author     ：vince
# Description：
"""
from core.reader.pdf import PdfDefaultTextReader

if __name__ == "__main__":
    file_path = 'attention is all you need.pdf'
    with open(file_path, 'rb') as file:
        res = PdfDefaultTextReader(file).read()
        print(res)