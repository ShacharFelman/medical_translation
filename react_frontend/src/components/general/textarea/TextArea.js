import { useRef} from "react";
import { useLanguage } from "../../../contexts/LanguageContext";
import { useTheme } from "../../../contexts/ThemeContext";
import "./textarea.css";
import ClearOutlinedIcon from '@mui/icons-material/ClearOutlined';  
import { Editor } from 'primereact/editor';

const renderCustomToolbar = () => {
    return (
        <div id="toolbar">
            <select className="ql-font"></select>
            <select className="ql-size"></select>
   
            <span className="ql-formats">
                <button className="ql-bold"></button>
                <button className="ql-italic"></button>
                <button className="ql-underline"></button>
                <button className="ql-strike"></button>
                <button className="ql-underline"></button>
            </span>
            <span className="ql-formats">                    
                <select className="ql-color"/>
                <select className="ql-background"/>                    
                <button className="ql-clean"></button>
            </span>         
                   


            <span className="ql-formats">
                <button className="ql-list" value="ordered"></button>
                <button className="ql-list" value="bullet"></button>
                <button className="ql-indent" value="-1"></button>
                <button className="ql-indent" value="+1"></button>
            </span>

            <span className="ql-formats">
                <button className="ql-direction" value="rtl"></button>
                <select className="ql-align"></select>
            </span>                

            <span className="ql-formats">
                <button className="ql-link"></button>
                <button className="ql-image"></button>
            </span>
            
        </div>
    );

}


const TextArea = ({value,valueText,onChange,placeholder="", maxLength,children}) => {
    
    const editorRef = useRef();

    const onClearClick = () => {
        onChange("","");
        setTimeout(() => {
            alignQuill();
          }, 0);        
        
    }


    const handleOnTextChange = (e) => {
        onChange && onChange(e.htmlValue,e.textValue)
        
    }

    const handlePaste = (event) => {
        setTimeout(() => {
            alignQuill();
        }, 0);        
    };

    const alignQuill = () => {
        if (editorRef.current){
            const quill = editorRef.current.getQuill()
            if (quill){
                quill.format("align","right");
                quill.format("direction","rtl");
            }      
            
        }
    }   
    const onEditorLoad = () => {
        alignQuill()
    }

    const onEditorClick = () => {
        if (editorRef.current) {
            const quill = editorRef.current.getQuill();
            if (quill) {
                quill.focus();
            }
        }
    };



    const renderTextLengthProgress = () => {
        let currentLength = 0;
        if (valueText){
            currentLength = valueText.length
        }
        return `${currentLength}/${maxLength}`
    }

    
    return (
        <div className="textarea-container">
            <div className="textarea-text-container">
                <Editor
                    onClick={onEditorClick}
                    // placeholder={placeholder}
                    ref={editorRef}
                    value={value} 
                    onTextChange={handleOnTextChange} 
                    style={{ 
                        backgroundColor:"white",
                        direction:"rtl",
                        textAlign:"right",
                        maxWidth:"100%",
                        width:"100%"
                    }} 
                    headerTemplate={renderCustomToolbar()}
                    onLoad={onEditorLoad}
                    onPaste={handlePaste}                    
                />            

                <div className="textarea-container-bottom-options">

                    <div className="textarea-chars-progress" >
                        {renderTextLengthProgress()}
                    </div>        

                    <div className="text-area-action-button">   
                        {children}
                    </div>

                </div>
                <div className="text-area-clear-button">
                    <ClearOutlinedIcon onClick={onClearClick}/>
                </div>                
            </div>

        </div>
    )
}

export default TextArea;