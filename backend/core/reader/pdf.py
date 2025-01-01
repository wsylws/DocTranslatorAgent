# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : pdf.py
# Time       ：2025/1/1 13:13
# Author     ：vince
# Description：
"""
from typing import List

import fitz
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTChar
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pymupdf import Document

from core.models.layout.yolo import YOLOLayout
from core.models.ocr.paddle import PaddleOCR
from core.reader.base import BaseReader
from core.vo import ReaderResult, TextBlock
from magic_pdf.config.ocr_content_type import BlockType
from magic_pdf.data.data_reader_writer import DataWriter
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.dict2md.ocr_mkcontent import merge_para_with_text
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze

class PdfTextReader(BaseReader):
    """
        Read text pdf
    """

    def read(self) -> List[ReaderResult]:
        result = []
        for page_no, page in enumerate(PDFPage.get_pages(self.file)):
            result.append(ReaderResult(page_no=page_no, text_blocks=self.read_from_page(page_no, page)))
        return result

    def __init__(self, file):
        super().__init__(file)
        resource_manager = PDFResourceManager()
        laparams = LAParams()
        self.device = PDFPageAggregator(resource_manager, laparams=laparams)
        self.page_interpreter = PDFPageInterpreter(resource_manager, self.device)
        self.doc = Document(stream=file.read())
        self.page_count = self.doc.page_count
        self.layout_model = YOLOLayout()


    def read_from_page(self, page_no, page):
        doc_page = self.doc.load_page(page_no)
        pix = doc_page.get_pixmap()
        text_blocks = self.layout_model.split_blocks(pix)

        self.page_interpreter.process_page(page)
        layout = self.device.get_result()
        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                text = element.get_text()
                x0, y0, x1, y1 = element.bbox
                x0, y0, x1, y1 = (
                    int(x0),
                    int(y0),
                    int(x1),
                    int(y1)
                )
                for block in text_blocks:
                    if (block.x0 <= x0 and block.six_y0 <= y0 and
                            block.x1 >= x1 and block.six_y1 >= y1):
                        block.text = block.text + text
                        block.font_size = self.get_max_font_size(element)
        return text_blocks

    def get_max_font_size(self, para):
        max_font_size = 0
        for obj in para:
            if isinstance(obj, LTChar):
                max_font_size = obj.size if obj.size > max_font_size else max_font_size
            elif hasattr(obj, '__iter__'):
                for sub_obj in obj:
                    if isinstance(sub_obj, LTChar):
                        max_font_size = sub_obj.size if sub_obj.size > max_font_size else max_font_size
        return max_font_size

class PdfOcrReader(BaseReader):
    """
        use YOLO 、paddleocr
    """

    def read(self) -> List[ReaderResult]:
        result = []
        for page_no, page in enumerate(PDFPage.get_pages(self.file)):
            result.append(ReaderResult(page_no=page_no, text_blocks=self.read_from_page(page_no, page)))
        return result

    def __init__(self, file):
        super().__init__(file)
        self.doc = Document(stream=file.read())
        self.page_count = self.doc.page_count
        self.layout_model = YOLOLayout()
        self.ocr_model = PaddleOCR()

    def read_from_page(self, page_no, page):
        doc_page = self.doc.load_page(page_no)
        pix = doc_page.get_pixmap()
        text_blocks = self.layout_model.split_blocks(pix)

        # Cutting small images for OCR
        for block in text_blocks:
            #
            react = fitz.Rect(block.x0 - 2, block.y0 - 2, block.x1 + 2, block.y1 + 2)
            clip = doc_page.get_pixmap(clip=react)
            text, font_size = self.ocr_model.ocr(clip.tobytes("png"))
            block.text = text
            block.font_size = font_size
        return text_blocks

class MinerUReader(BaseReader):
    """
        see https://github.com/opendatalab/MinerU
    """

    @staticmethod
    def mineru_block_to_text_block(block, is_bold) -> TextBlock:
        print(block)
        bbox = block['bbox']
        # Font size is taken from the first line
        first_line_bbox = block['lines'][0]['bbox']
        font_size = first_line_bbox[3] - first_line_bbox[1]
        text_block = TextBlock(x0=bbox[0],
                               y0=bbox[1],
                               x1=bbox[2],
                               y1=bbox[3],
                               text=merge_para_with_text(block),
                               type='text',
                               font_size=font_size,
                               is_bold=is_bold
                               )
        return text_block

    @staticmethod
    def para_to_text_block(para_block) -> List[TextBlock]:
        para_type = para_block['type']
        text_blocks = []
        if para_type in [BlockType.Text, BlockType.List, BlockType.Index, BlockType.Title] and para_block['lines']:
            text_blocks.append(MinerUReader.mineru_block_to_text_block(para_block, para_type == BlockType.Title))
        elif para_type == BlockType.Image:
            for block in para_block['blocks']:
                if block['type'] == BlockType.ImageCaption and block['lines']:
                    text_blocks.append(MinerUReader.mineru_block_to_text_block(block, True))
                if block['type'] == BlockType.ImageFootnote and block['lines']:
                    text_blocks.append(MinerUReader.mineru_block_to_text_block(block, False))
        elif para_type == BlockType.Table:
            for block in para_block['blocks']:
                if block['type'] == BlockType.TableCaption and block['lines']:
                    text_blocks.append(MinerUReader.mineru_block_to_text_block(block, True))
                if block['type'] == BlockType.TableFootnote and block['lines']:
                    text_blocks.append(MinerUReader.mineru_block_to_text_block(block, False))

        return text_blocks

    @staticmethod
    def info_dict_to_result(pdf_info_dict: list) -> List[ReaderResult]:
        results = []

        for page_info in pdf_info_dict:
            paras_of_layout = page_info.get('para_blocks')
            page_idx = page_info.get('page_idx')
            text_blocks = []
            if not paras_of_layout:
                continue
            for para_block in paras_of_layout:
                text_blocks.extend(MinerUReader.para_to_text_block(para_block))
            page_result = ReaderResult(page_no=page_idx, text_blocks=text_blocks)
            results.append(page_result)
        return results


    def read(self) -> List[ReaderResult]:

        # No need to write img
        class NoneWriter(DataWriter):

            def write(self, path: str, data: bytes) -> None:
                pass

        image_writer = NoneWriter()

        ds = PymuDocDataset(self.file.read())

        infer_result = ds.apply(doc_analyze, ocr=True)

        pipe_result = infer_result.pipe_ocr_mode(image_writer)

        res = MinerUReader.info_dict_to_result(pipe_result._pipe_res['pdf_info'])
        return res