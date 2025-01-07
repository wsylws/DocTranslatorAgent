# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : paddle.py
# Time       ：2025/1/1 15:41
# Author     ：vince
# Description：
"""
from paddleocr import PaddleOCR as Paddle

ocr = Paddle(use_angle_cls=True, lang='en')

class PaddleOCR:

    def ocr(self, img) -> [str, float]:
        result = ocr.ocr(img, cls=True)

        def sort_and_merge_ocr_results(ocr_results):
            if not ocr_results[0] or not ocr_results[0][0] or not ocr_results[0][0][0]:
                return "", 0
            # Font taken from the first line y1-y0
            x0, y0 = ocr_results[0][0][0][0]
            x1, y1 = ocr_results[0][0][0][2]
            size = y1 - y0

            flat_results = [
                (result[0][0][1], result[0][0][0], result[1][0])  # (top, left, text)
                for result in ocr_results[0]  # Assuming the structure is as given
            ]

            # Sort the text boxes by their top coordinates. If the top coordinates are the same, sort them by their left coordinates
            sorted_results = sorted(flat_results, key=lambda x: (round(x[0]), x[1]))

            # Merge Text
            merged_text = '\n'.join([text for _, _, text in sorted_results])
            return merged_text, size

        result_text, font_size =    sort_and_merge_ocr_results(result)
        return result_text, font_size
