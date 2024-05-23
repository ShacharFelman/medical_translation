import { useEffect, useRef, useState } from "react";
import "./output-text.css";
import { toast } from "react-toastify";
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import { IconButton } from "@mui/material";
import { useTheme } from "../../contexts/ThemeContext";
import { useLanguage } from "../../contexts/LanguageContext";
import LoadingVideo from "../general/loading-video/LoadingVideo";
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


const OutputText = ({text, placeholder,loading,onOutputTextChange}) => {
    const {theme} = useTheme()
    const [onlyText,setOnlyText] = useState(text);
    const {language} = useLanguage();
    const editorRef = useRef();
    


    useEffect(() => {
        setOnlyText(text)
    },[text])

    const handleOnTextChange = (event) => {
        onOutputTextChange(event.htmlValue)
        setOnlyText(event.textValue)

    }

    const copyToClipboard = (event) => {
        navigator.clipboard.writeText(editorRef.current.getContent().innerText)
            .then(() => {
                toast.success(language.successfulCopy(),{
                    autoClose:1000
                })
            })
            .catch((error) => {
                console.error('Error copying to clipboard:', error)
                toast.error("fail to copy text!",{
                    autoClose:300
                })
            });
    };


    const alignQuill = () => {
        if (editorRef.current){
            const quill = editorRef.current.getQuill()
            if (quill){
                quill.format("align","left");
                quill.format("direction","ltr");
            }        
            
        }
    }

    const onEditorLoad = () => {
        setTimeout(() => {
            alignQuill();
          }, 0);    
    }

    return (
        <div className="output-text-container" style={{
            ...theme.components.input.output
        }}> 
            <div className="output-text">
                {loading ? (
                    <div className="output-text-loading" >
                        <LoadingVideo/>
                    </div>
                ): text && text.length > 0 
                    ? (
                        <Editor 
                            ref={editorRef}
                            headerTemplate={renderCustomToolbar()}
                            value={text} 
                            onTextChange={handleOnTextChange} 
                            style={{ 
                                backgroundColor:"#f0f0f0",
                                direction:"ltr",
                                textAlign:"left",
                                height:"40vh"
                            }} 
                            onLoad={onEditorLoad}
                            />           
                    )
                    :(
                        <div className="output-text-placeholder" style={{
                            ...theme.components.input.outputPlaceholder
                        }}>
                            {placeholder}
                        </div>
                    )   
                }
            </div>
            {!loading  && text && text.length > 0 && (
                <div className="copy-button">
                    <IconButton onClick={copyToClipboard}>
                        <ContentCopyIcon />
                    </IconButton>
                </div>
            )}
        </div>

    )
}   

export default OutputText;