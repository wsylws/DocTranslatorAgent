 [English](README.md) | 简体中文
# DocTranslaterAgent

开发中

## 项目依赖

### reader依赖
- [DocLayout-YOLO](https://github.com/opendatalab/DocLayout-YOLO)
- [MinerU](https://github.com/opendatalab/MinerU)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

## 快速开始
```
pip install -r requirements.txt
```
## 核心代码
- BaseReader--pdf文本块读取
  - PdfTextReader： 文本类型pdf阅读器，基于YOLO识别出文本区块，通过pdfminer获取区块文本信息
  - PdfOcrReader： 图片类型pdf阅读器，基于YOLO识别出文本区块，通过paddleocr识别区块文本信息
  - MinerUReader： 解析MinerU返回结果，构建区块信息
- BaseTranslator--文本批量翻译
  - LlmTranslator：大模型翻译器