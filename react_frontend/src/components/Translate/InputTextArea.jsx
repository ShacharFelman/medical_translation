import React, { useEffect, useRef } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import TranslateButton from "../Buttons/TranslateButton";

export default function InputTextArea({inputText, onChange, onClickTranslate, isTranslating}) {
  const quillRef = useRef(null);

  const modules = {
    toolbar: [
      [{ 'header': [1, 2, 3, false] }],
      ['bold', 'italic', 'underline'],
      [{'list': 'ordered'}, {'list': 'bullet'}],
      [{ 'align': [] }],
    ]
  };

  const formats = [
    'header', 'font', 'size',
    'bold', 'italic', 'underline', 'strike',
    'list', 'bullet', 'indent',
    'link', 'image',
    'align', 'direction'
  ];

  useEffect(() => {
    if (quillRef.current) {
      const editor = quillRef.current.getEditor();
      
      const formatAllContent = () => {
        const length = editor.getLength();
        editor.formatLine(0, length, 'direction', 'rtl');
        editor.formatLine(0, length, 'align', 'right');
      };

      formatAllContent();

      editor.on('text-change', function(delta, oldDelta, source) {
        if (source === 'user') {
          formatAllContent();
        }
      });
    }
  }, []);

  const handleChange = (content, delta, source, editor) => {
    onChange(content);
  };
  
  return (
    <div className="flex flex-col flex-grow space-y-2 w-2/12">
      <div className="rounded-md border w-full h-56 text-black bg-gray-50 overflow-hidden">
        <ReactQuill 
          ref={quillRef}
          theme="snow"
          value={inputText}
          onChange={handleChange}
          modules={modules}
          formats={formats}
          placeholder='...הכנס טקסט רפואי לתרגום כאן'
          className="flex flex-col h-full
                    [&_.ql-container]:overflow-hidden
                    [&_.ql-editor.ql-blank::before]:text-right
                    [&_.ql-editor_h1]:font-bold [&_.ql-editor_h1]:underline [&_.ql-editor_h1]:text-xl
                    [&_.ql-editor_h2]:font-bold [&_.ql-editor_h2]:text-lg"
        />
      </div>
      <div id="actions" className="mt-2">
        <TranslateButton 
          title={isTranslating ? "Translating..." : "Translate"}
          onClick={onClickTranslate}
          disabled={isTranslating}
        />
      </div>
    </div>
  );
}