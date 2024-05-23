import { useCallback, useState } from "react";
import "./reference-file-upload.css";
import { IconButton } from "@mui/material";
import UploadIcon from '@mui/icons-material/Upload';
import { useApi } from "../../contexts/ApiContext";
import { useLanguage } from "../../contexts/LanguageContext";
import { toast } from 'react-toastify';

import Dropzone from 'react-dropzone'
import { useTheme } from "../../contexts/ThemeContext";

const ReferenceFileUpload = () => {
    const {theme} = useTheme();
    const {uploadReferenceFile,referenceToken} = useApi();
    const {language,isRTL} = useLanguage()
    const [referenceFile,setReferenceFile]  = useState(null);
    const [loading,setLoading]  = useState(false);

    const referenceFileLabel = language.referenceFileLabelText();
    const supportedFileTypeLabel = language.supportedFilesText() 
    const browseFilesLabel = language.browseFilesText();
    const dragAndDropLabel = language.dragAndDropFileText();
    const  orLabel = language.orText();
    
    const uploadReference = async () => {
        await uploadReferenceFile(referenceFile);
    }

    const onFileDrop = useCallback(acceptedFiles => {
        setReferenceFile(acceptedFiles[0])
      }, [])



    const flexDirection = isRTL ? "row-reverse" : "row" ;
    const textAlign = isRTL ? "right" : "left"

    
    
    
    return (
        <div className="reference-file-upload-container" style={{
            flexDirection:flexDirection,
            
        }}>
            <div className="reference-file-text-container"  style={{                
                flex:1,
                display:"flex", 
                textAlign:textAlign,
            }}>
                <div style={{
                    flex:1,
                    flexDirection:"column"
                }}>
                    <label   className="reference-file-text-label">
                            {referenceFileLabel}
                    </label>
                    <div>
                        <label>{supportedFileTypeLabel}</label>
                    </div>
                </div>

            </div>

            <div className="reference-file-drop-container" style={{
                flex:1, 
                justifyContent:"center",
                alignItems:"center",    
                display:"flex",
                
            }}>

                <div   style={{
                    display:"flex",
                    flexDirection:"row",

                    
                }}>

                
                    <Dropzone
                        onDrop={onFileDrop}>
                            {({getRootProps, getInputProps}) => (
                                <div className="reference-file-box" {...getRootProps()}>
                                    <input {...getInputProps()} />
                                    <div className="reference-typography" >
                                        {dragAndDropLabel}
                                    </div>
                                    
                                    <div className="reference-file-box-seperator-container"> 
                                        <div className="reference-file-box-line-container">
                                            <div className="reference-file-box-line"/>
                                        </div>
                                        <p className="reference-typography" >
                                            {orLabel}
                                        </p>
                                        <div className="reference-file-box-line-container"> 
                                            <div className="reference-file-box-line"/>
                                        </div>

                                    </div>
                                    <div className="reference-file-box-file-button-container">
                                        <div className="reference-file-box-file-button-text"  style={{
                                            ...theme.components.button.alt_primary                        
                                        }}>
                                            {referenceFile === null ? browseFilesLabel: referenceFile.path}
                                        </div>
                                    </div>
                                    
                                
                                </div>
                        )}
                    </Dropzone>
                    <IconButton onClick={uploadReference}>
                    <UploadIcon/>
                </IconButton>                    
                </div>

            </div>     
            <div style={{
                flex:1,
                display:"flex",

            }}>


            </div>
        </div>
    )
}
export default ReferenceFileUpload;