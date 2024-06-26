import React, { useState } from 'react';
import TranslateButton from './Buttons/TranslateButton';
import AddButton from './Buttons/AddButton';
import { Add } from '@mui/icons-material';
import DeleteButton from './Buttons/DeleteButton';



export default function TranslateSection({ getTranslation, onDelete}) {
//plainText is the text that the user types in the textarea should send outside
//translate is the text after translation - should recieve from outside
  const [plainText, setPlainText] = useState(''); 
  const [translate, setTranslate] = useState('Translated Text Here...');

  function handleTextToTranslate(event){
    setPlainText(event.target.value);
  }  
  
  function handleTranslate() {
    setTranslate(getTranslation(plainText));
    // setTranslate("English: "+plainText);
  }

  return (
    <ul className="flex space-x-5 place-content-center mb-8">
      <li className="flex flex-col space-y-2">
        <select className="rounded-md border p-2 w-64 md:w-96 h-10 bg-white text-black">
          <option>English</option>
        </select>
        {/* <card className="items-center"><p>English</p></card> */}
        <textarea 
          className= "rounded-md border p-2 w-64 md:w-96 h-56 text-black bg-gray-200" 
          type="text" 
          value={translate} 
          readOnly 
        /> 
      </li>
      <li className="flex flex-col space-y-2">
        <select className="rounded-md border p-2 w-64 md:w-96 h-10 bg-white text-black">
          <option>Hebrew</option>
        </select>
        {/* <card><p>Hebrew</p></card> */}
        <textarea 
          className= "rounded-md border p-2 w-64 md:w-96 h-56 text-black bg-gray-50"  
          type="text" value={plainText} 
          onChange={handleTextToTranslate}
        /> 
        <p id="actions">
        <TranslateButton title="Translate" onClick={handleTranslate}/>
        </p>
      </li>
      <li className="flex flex-col">
        <DeleteButton onClick={onDelete}/>
      </li>
    </ul>

  );
}