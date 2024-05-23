import ParagraphItem from "../item"
import "./paragraph-list-item.css";
import DeleteButton from "../../delete-button";
import { useLanguage } from "../../../../../../../contexts/LanguageContext";
import { useEffect } from "react";


const ParagraphListItem = ({id,paragraphIndex,textInput,textInputRawText,deleteable,onDelete,onTextInputChange,outputText,loading,onOutputTextChange,translateTextInput}) => {
    
    const handleOnDeleteParagraph = () => {
        onDelete()
    }

    const {isRTL} = useLanguage();
    // const flexDirection = isRTL ? "row-reverse" : "row";
    const flexDirection = "row-reverse" ;
    
    return (
        <div className="paragraph-list-item-container" id={id} style={
            {
                flexDirection:flexDirection
            }
        }>
            <div className="paragraph-list-body-container">
                <DeleteButton onDelete={handleOnDeleteParagraph} deleteable={deleteable}/>
                <ParagraphItem
                    paragraphIndex={paragraphIndex}
                    textInput={textInput}
                    textInputRawText={textInputRawText}
                    onTextInputChange={onTextInputChange}
                    onOutputTextChange={onOutputTextChange}
                    isLoading={loading}
                    outputText={outputText}
                    translateTextInput={translateTextInput}
                />
                
            </div>


        </div>
    )
}

export default ParagraphListItem