// src/pages/Pdf/index.js
import React, { useEffect, useState } from 'react';
import api from '../../api/index';
import './styles.css'; // 导入自定义样式文件
import PdfView from './pdfView';
  
const MyDocument = () => {
  const [file, setFile] = useState('');
  const [fileStrem, setFileStrem] = useState(null);
  const [selectedReader, setSelectedReader] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedTranslator, setSelectedTranslator] = useState(null);
  const [readers, setReaders] = useState([]);
  const [translators, setTranslators] = useState([]);
  const [textBlock, setTextBlock] = useState([])
  const [languageList, setLanguageList] = useState([]);
  const [sourceLang, setSourceLang] = useState('English');
  const [targetLang, setTargetLang] = useState('Chinese');
  const [error, setError] = useState(''); 

  useEffect(() => {
    getReaders();
    getTranslators();
    getLanguage()
  }, []);

  // 获取翻译器类型列表
  const getReaders = async () => {
    try {
      const res = await api.get('/readers');
      // res.data 是一个包含 选择翻译类型 的数组
      setReaders(res);
    } catch (err) {
      console.error('Error fetching readers:', err);
    }
  };

  // 获取翻译器列表
  const getTranslators = async () => {
    try {
      const res = await api.get('/translators');
      setTranslators(res);
    } catch (err) {
      console.error('Error fetching readers:', err);
    }
  };

  // 获取翻译器列表
  const getLanguage = async () => {
    try {
      const res = await api.get('/support_language');
      setLanguageList(res);
    } catch (err) {
      console.error('Error fetching readers:', err);
    }
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      setFileStrem(selectedFile);
      const fileReader = new FileReader();
      fileReader.onload = (e) => {
        setFile(e.target.result);
      };
      fileReader.readAsDataURL(selectedFile);
    }
  };

  const handleReadersSelectChange = (event) => {
    const selectedValue = event.target.value;
    setSelectedReader(selectedValue);
  };

  const handleTranslatorSelectChange = (event) => {
    const selectedValue = event.target.value;
    setSelectedTranslator(selectedValue);
  };

  const handleSourceSelectChange = (event) => {
    const selectedValue = event.target.value;
    setSourceLang(selectedValue);
  };

  const handleTargetSelectChange = (event) => {
    const selectedValue = event.target.value;
    setTargetLang(selectedValue);
  };

  const handleUpload = async () => {
    // 处理上传逻辑
    if (!fileStrem) {
      setError('Please select a PDF file.');
      return;
    }
    if (!selectedReader) {
      setError('Please select a reader.');
      return;
    }
    if (!selectedTranslator) {
      setError('Please select a translator.');
      return;
    }
    if (!sourceLang) {
      setError('Please select a source language.');
      return;
    }
    if (!targetLang) {
      setError('Please select a target language.');
      return;
    }
    const formData = new FormData();
    formData.append('file', fileStrem);
    formData.append('reader_name', selectedReader);
    setLoading(true)
    try {
      const res = await api.post('/get_text_block',formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setTextBlock(res)
      console.log(res)
    } catch(err) {}
    setLoading(false)
  };
  
  if (textBlock.length) {
    return (
      <PdfView 
        textBlock={textBlock}
        file={file} 
        reader={selectedReader}
        translator={selectedTranslator}
        sourceLang={sourceLang}
        targetLang={targetLang}
      ></PdfView>
    );
  } else {
    return (
      <div className="container">
        {
        loading ?  <div className="loading-overlay">
            <div className="loading-spinner"></div>
        </div> : null
        }
        <div>
          <p>Please upload a PDF and select one from the dropdown.</p>
          <input
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="input-style"
          />
          <select
            value={selectedReader || ''}
            onChange={handleReadersSelectChange}
            className="select-style"
          >
            <option value="">Select a readers</option>
            {readers.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
          <select
            value={selectedTranslator || ''}
            onChange={handleTranslatorSelectChange}
            className="select-style"
          >
            <option value="">Select a translator</option>
            {translators.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
          <select
            value={sourceLang || ''}
            onChange={handleSourceSelectChange}
            className="select-style"
          >
            <option value="">Select source lang</option>
            {languageList.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <select
            value={targetLang || ''}
            onChange={handleTargetSelectChange}
            className="select-style"
          >
            <option value="">Select target lang</option>
            {languageList.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <button onClick={handleUpload} className="button-style">
            Upload PDF
          </button>
          {error && <div className="error-message">{error}</div>} {/* 显示错误提示 */}
        </div>
      </div>
    );  
  }
};

export default MyDocument;