import React, { useState , useEffect, useContext} from 'react';
import DeleteButton from '../Buttons/DeleteButton';
import OutputTextArea from './OutputTextArea';
import InputTextArea from './InputTextArea';
import { TranslateContext } from '../../store/TranslateContext.jsx';

export default function TranslateSection({inputText, 
                                          translation, 
                                          onDelete, 
                                          onInputChange, 
                                          onTranslate}) {
                                            
  const {getTranslation} = useContext(TranslateContext);
  const [localInputText, setLocalInputText] = useState(inputText);

   // Synchronize localInputText with the inputText prop
  useEffect(() => {
    setLocalInputText(inputText);
  }, [inputText]);


    function handleTextToTranslate(event){
      const newText = event.target.value;
      setLocalInputText(newText);
      onInputChange(newText);
    }  
    
    function handleTranslate() {
      const newTranslation = getTranslation(localInputText);
      onTranslate(newTranslation);
    }
  
     return (
      <div className="relative flex flex-grow space-x-5 mb-8">
        <OutputTextArea translation= {translation}/>
        <InputTextArea inputText={inputText} onChange={handleTextToTranslate} onClickTranslate={handleTranslate}/>
        <DeleteButton onClick={onDelete} />
      </div>
    );
  }
