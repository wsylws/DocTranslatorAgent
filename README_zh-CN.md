 [English](README.md) | 简体中文
# DocTranslaterAgent

## 项目结构
- backend 后端项目
  - python3.10
- web 前端项目(开发中)

## 核心代码
- BaseReader--pdf文本块读取
  - PdfDefaultTextReader： 默认文本类型pdf阅读器，基于YOLO识别出文本区块，通过pdfminer获取区块文本信息
  - PdfDefaultOcrReader： 默认图片类型pdf阅读器，基于YOLO识别出文本区块，通过paddleocr识别区块文本信息
  - MinerUReader（推荐）： 解析MinerU返回结果，构建区块信息（支持公式识别，OCR结果准确率较高）
    - MinerOcrUReader: 使用ocr解析
    - MinerTextUReader: 文本pdf解析，省去ocr步骤
- BaseTranslator--文本批量翻译
  - LlmTranslator：大模型翻译器（对应配置 llm、openai）
  - BaiduTranslator: 百度翻译器（对应配置 baidu）
- Configuration--配置管理

## 快速开始
### 后端项目
1. 依赖安装
```
pip install -r requirements.txt --extra-index-url https://wheels.myhloli.com -i https://mirrors.aliyun.com/pypi/simple
```
2. 模型安装
  - juliozhao/DocLayout-YOLO-DocStructBench 国内推荐使用镜像站加载
  - minerU [模型权重文件安装](https://mineru.readthedocs.io/zh-cn/latest/user_guide/install/download_model_weight_files.html)（使用MinerUReader时需要）

国内推荐使用镜像站安装
```commandline
pip install huggingface_hub
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download 

-
```
3. 工作目录设置为backend/api（如使用Pycharm启动） 或 cd backend/api（命令行启动）
4. 添加backend目录为PYTHONPATH
5. 启动项目
```commandline
python app.py
```

### 前端项目
开发中


## 外部引用
- [DocLayout-YOLO](https://github.com/opendatalab/DocLayout-YOLO)
- [MinerU](https://github.com/opendatalab/MinerU)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)