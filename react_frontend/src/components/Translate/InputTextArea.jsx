import TranslateButton from "../Buttons/TranslateButton";
export default function InputTextArea({inputText, onChange, onClickTranslate,isTranslating}){
    return(
      <div className="flex flex-col flex-grow space-y-2">
        <textarea 
          className="rounded-md border p-2 w-full h-56 text-black bg-gray-50" 
          type="text" 
          value={inputText} 
          placeholder='הכנס טקסט רפואי לתרגום כאן...'
          onChange={onChange}
          dir= "rtl"
        /> 
        <div id="actions" className="mt-2">
          <TranslateButton 
            title={isTranslating ? "Translating..." :"Translate" }
            onClick={onClickTranslate}
            disabled={isTranslating} />
        </div>
      </div>
    );
}