import React from 'react';
import TranslateButton from "../Buttons/TranslateButton";
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';

export default function InputTextArea({inputText, onChange, onClickTranslate,isTranslating}){
  const modules = {
    toolbar: [
      [{ 'header': [1, 2, false] }],
      ['bold', 'italic', 'underline', 'strike'],
      [{'list': 'ordered'}, {'list': 'bullet'}, {'indent': '-1'}, {'indent': '+1'}],
      ['link', 'image'],
      ['clean']
    ],
  };

  const formats = [
    'header', 'bold', 'italic', 'underline', 'strike',
    'list', 'bullet', 'indent', 'link', 'image'
  ];  

  const handleChange = (content) => {
    onChange(content);
  };
  
  return(
      <div className="flex flex-col flex-grow space-y-2 w-2/12">
        {/* <textarea 
          className="rounded-md border p-2 w-full h-56 text-black bg-gray-50" 
          type="text" 
          value={inputText} 
          placeholder='הכנס טקסט רפואי לתרגום כאן...'
          onChange={onChange}
          dir= "rtl"
        />  */}
        <div className="rounded-md border w-full h-56 text-black bg-gray-50 overflow-hidden">
          <div className="rounded-md border w-full h-56 text-black bg-gray-50 overflow-hidden [&_.ql-editor]:text-right [&_.ql-editor]:rtl [&_.ql-editor.ql-blank::before]:right-0 [&_.ql-editor.ql-blank::before]:left-auto [&_.ql-editor.ql-blank::before]:text-right">
            <ReactQuill 
              theme="snow"
              value={inputText}
              onChange={handleChange}
              modules={modules}
              formats={formats}
              placeholder='הכנס טקסט רפואי לתרגום כאן...'
              className="h-full" 
            />
          </div>
        </div>
        <div id="actions" className="mt-2">
          <TranslateButton 
            title={isTranslating ? "Translating..." :"Translate" }
            onClick={onClickTranslate}
            disabled={isTranslating} />
        </div>
      </div>
    );
}