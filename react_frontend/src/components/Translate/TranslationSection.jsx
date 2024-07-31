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
  const [isTranslating, setIsTranslating] = useState(false);

   // Synchronize localInputText with the inputText prop
  useEffect(() => {
    setLocalInputText(inputText);
  }, [inputText]);


    // function handleTextToTranslate(event){
    //   const newText = event.target.value;
    //   setLocalInputText(newText);
    //   onInputChange(newText);
    // }  
    
    function handleTextToTranslate(newText){
      setLocalInputText(newText);
      onInputChange(newText);
    }  
    
    async function handleTranslate() {
      setIsTranslating(true);
      try{
        const newTranslation = await getTranslation(localInputText);
        onTranslate(newTranslation);
      }
      catch(error){
        console.error('Error translating paragraph:', error);
      }
      finally{
        setIsTranslating(false);
      }
    }
  
     return (
      <div className="relative flex flex-grow space-x-5 mb-8">
        <OutputTextArea translation= {translation} isTranslating= {isTranslating}/>
        <InputTextArea inputText={localInputText} onChange={handleTextToTranslate} onClickTranslate={handleTranslate} isTranslating= {isTranslating}/>
        <DeleteButton onClick={onDelete} className= "flex items-start" />
      </div>
    );
  }
