import React, { useEffect, useState, useRef, memo } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css'; // 导入 TextLayer 的 CSS 文件
import './pdf.css'; // 导入自定义样式文件

// @ts-expect-error This does not exist outside of polyfill which this is doing
if (typeof Promise.withResolvers === 'undefined') {
  if (window)
    // @ts-expect-error This does not exist outside of polyfill which this is doing
    window.Promise.withResolvers = function () {
      let resolve, reject;
      const promise = new Promise((res, rej) => {
        resolve = res;
        reject = rej;
      });
      return { promise, resolve, reject };
    };
}

// 加载 pdf.js 工具
pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/legacy/build/pdf.worker.min.mjs',
  import.meta.url
).toString();

const useTranslatedText = (text) => {
  const [parsedText, setParsedText] = useState(text);

  const parseMathJax = (text) => {
    const inlineMathPattern = /(\$\$?)(?!<)[^\$]+(?<!\$)\1|\\\((.*?)\\\)/g;
    const blockMathPattern = /\$\$(.*?)\$\$|\\\[(.*?)\\\]/gs;

    // 替换行内公式
    let result = text.replace(inlineMathPattern, (match) => (
      `<span class="math-inline">${match}</span>`
    ));

    // 替换块级公式
    result = result.replace(blockMathPattern, (match) => (
      `<div class="math-block">${match}</div>`
    ));
    return result;
  };

  useEffect(() => {
    if (text) {
      const parsed = parseMathJax(text);
      setParsedText(parsed);
    }
  }, [text]);

  useEffect(() => {
    if (window.MathJax && parsedText) {
      window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub]);
    }
  }, [parsedText]);

  return parsedText;
};

const TranslatedText = memo(({ item, page, index }) => {
  const parsedText = useTranslatedText(item.translate_text);

  return (
    <div key={`translated_text_${index}`}
      className="overlay translate-overlay"
      style={{
        left: item.x0 * 100 + '%',
        top: item.y0 * 100 + '%',
        width: (item.x1 - item.x0) * 100 + '%',
        height: (item.y1 - item.y0) * 100 + '%',
      }}>
      <div className="overlay-container">
        <div className="paragraph-element"
          style={{
            fontSize: item.font_size + 'px',
            fontWeight: item.is_bold ? 'bold' : 'normal'
          }}
        >
          <div dangerouslySetInnerHTML={{ __html: parsedText }}></div>
        </div>
      </div>
    </div>
  );
});

const PdfView = (props) => {
  const [numPages, setNumPages] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [translatedTexts, setTranslatedTexts] = useState({});
  const [loadingPages, setLoadingPages] = useState({});
  const containerRef = useRef(null);
  const documentRef = useRef(null);


  const onDocumentLoadSuccess = ({ numPages }) => {
    console.log(`Number of pages: ${numPages}`);
    setNumPages(numPages);
  };

  const handleScroll = () => {
    if (!containerRef.current || !numPages) return;
    const container = containerRef.current;
    const documentHeight = documentRef.current.clientHeight;
    const scrollTop = container.scrollTop;
    // 计算每页的高度
    const pageHeight = documentHeight / numPages;
    const newPage = Math.floor(scrollTop / pageHeight) + 1;

    setCurrentPage(newPage);
  };

  useEffect(() => {
    // 添加滚动事件监听器
    const container = containerRef.current;
    if (container) {
      container.addEventListener('scroll', handleScroll);
    }

    // 清理事件监听器
    return () => {
      if (container) {
        container.removeEventListener('scroll', handleScroll);
      }
    };
  }, [numPages]);

  useEffect(() => {
    // 在页面变化时请求接口
    if (!translatedTexts[currentPage]) {
      translate();
    }
  }, [currentPage]);

  const translate = async () => {
    let index = 0;
    props.textBlock.map((item, i) => {
      if (item.page_no === currentPage - 1) {
        index = i;
      }
    });

    const texts = props.textBlock[index].text_blocks;

    setLoadingPages(prevLoadingPages => ({
      ...prevLoadingPages,
      [currentPage]: true
    }));

    // 逐步更新翻译内容
    setTranslatedTexts(prevTranslatedTexts => ({
      ...prevTranslatedTexts,
      [currentPage]: []
    }));
    try {
      const response = await fetch('http://192.168.0.107:8000/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          texts: texts.map(item => item.text),
          source_lang: props.sourceLang,
          target_lang: props.targetLang,
          translator: props.translator
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let translatedTexts = [];

      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          break;
        }
        const chunk = decoder.decode(value, { stream: true });

        // 解析每个字段
        const lines = chunk.split('\n').filter(line => line.trim() !== '');
        for (const line of lines) {
          const data = JSON.parse(line);
          if (data) {
            translatedTexts.push({
              ...texts[data.index],
              translate_text: data.result
            });
            // 逐步更新翻译内容
            setTranslatedTexts(prevTranslatedTexts => ({
              ...prevTranslatedTexts,
              [currentPage]: translatedTexts
            }));
          }
        }

        // 加载完成，移除加载指示器
        setLoadingPages(prevLoadingPages => ({
          ...prevLoadingPages,
          [currentPage]: false
        }));
      }
    } catch (err) {
      // 加载完成，移除加载指示器
      setLoadingPages(prevLoadingPages => ({
        ...prevLoadingPages,
        [currentPage]: false
      }));

      // 逐步更新翻译内容
      setTranslatedTexts(prevTranslatedTexts => ({
        ...prevTranslatedTexts,
        [currentPage]: null
      }));

      console.error('Error translating PDF:', err);
    }
  };


  return (
    <div className="pdf-container">
      <div className="pdf-columns" ref={containerRef}>
        <div className="pdf-column" ref={documentRef}>
          <Document
            file={props.file}
            onLoadSuccess={onDocumentLoadSuccess}
          >
            {Array.from({ length: numPages }, (_, index) => (
              <Page
                key={`original_page_${index + 1}`}
                pageNumber={index + 1}
              />
            ))}
          </Document>
        </div>
        <div className="pdf-column">
          <Document
            file={props.file}
            onLoadSuccess={onDocumentLoadSuccess}
          >
            {Array.from({ length: numPages }, (_, index) => (
              <div key={`translated_page_${index + 1}`}>
                <Page
                  key={`translated_page_${index + 1}`}
                  pageNumber={index + 1}
                >
                  {
                    loadingPages[index + 1] && (
                      <div className="overlay loading-overlay">
                        <div className="loading-spinner"></div>
                        <div className="loading-text">翻译中</div>
                      </div>
                    )
                  }
                  {
                    translatedTexts[index + 1] &&
                    translatedTexts[index + 1].map((item, i) => (
                      <TranslatedText
                        key={`translated_text_${i}`}
                        item={item}
                        page={index + 1}
                        index={i}
                      />
                    ))
                  }
                </Page>
              </div>
            ))}
          </Document>
        </div>
      </div>
    </div>
  );
};

export default PdfView;