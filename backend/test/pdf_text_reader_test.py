# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : pdf_text_reader_test.py
# Time       ：2025/1/1 14:41
# Author     ：vince
# Description：
"""
from core.reader.pdf import PdfTextReader

if __name__ == "__main__":
    file_path = 'C:/Users/41593/Downloads/attention is all you need.pdf'
    with open(file_path, 'rb') as file:
        res = PdfTextReader(file).read()
        print(res)