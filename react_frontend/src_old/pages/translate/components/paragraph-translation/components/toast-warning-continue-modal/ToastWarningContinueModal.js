
import { useLanguage } from "../../../../../../contexts/LanguageContext";
import "./toast-warning-continue-modal.css";
import RefreshOutlinedIcon from '@mui/icons-material/RefreshOutlined';

const ToastWarningContinueModal = ({onCancelClick,onContinueClick}) => {
    const {isRTL,language} = useLanguage()
    return (
        <div style={{
            borderRadius:10
        }}>
            <div style={{
                textAlign:"center"
            }}>
            <RefreshOutlinedIcon/>
            </div>
                
            <div style={{
                fontSize:30,
                textAlign:'center',
            }}>
                {language.warningText()}
            </div> 
            <p style={isRTL ? {
                textAlign:"right"
            } : {
                textAlign:"left"
            }}>{language.referenceFileNotUploadWarningText()}</p>
            <div style={{
                display:"flex",
                justifyContent:"space-evenly"
            }}>
                <button style={{
                    backgroundColor:"yellow",
                    borderRadius:5,
                    padding:5
                }} className="toast-warning-continue-modal-button-continue" onClick={onContinueClick}>{language.continueText()}</button>
                <button  style={{
                    backgroundColor:"lightgreen",
                    borderRadius:5,
                    padding:5,
                    
                }} className="toast-warning-continue-modal-button-cancel" onClick={onCancelClick}>{language.cancelText()}</button>                
            </div>

        </div>
    )   
}

export default ToastWarningContinueModal;