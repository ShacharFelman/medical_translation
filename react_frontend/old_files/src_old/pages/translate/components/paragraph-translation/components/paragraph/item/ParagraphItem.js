import "./paragraph.css";
import React from "react";
import { useLanguage } from "../../../../../../../contexts/LanguageContext";
import OutputText from "../../../../../../../components/output-text";
import TextArea from "../../../../../../../components/general/textarea/TextArea";
import TranslateButton from "../../translate-button";

const ParagraphItem =({
    paragraphIndex,
    textInput,
    textInputRawText,
    onTextInputChange,
    isLoading,
    outputText,
    onOutputTextChange,
    translateTextInput

}) => {
    const {language} = useLanguage();
    const maxInputLength = 4096 / 4
    const outputTextPlaceholder = language.translationText();

    const handleOnTextInputChange = (value,text) => {
        onTextInputChange(value,text);
    }

    const flexDirection = "row-reverse";

    return (
        <div className="paragraph-item-container">

            
            <div className="paragraph-container" style={{
            }}>
                <div className="paragraphs-container" style={{
                    flexDirection:flexDirection
                }}>
                    <div className="pargraph-text-input-container">
                        
                        <TextArea
                            value={textInput}  
                            valueText={textInputRawText}
                            maxLength={maxInputLength}
                            onChange={handleOnTextInputChange}
                            placeholder={language.textInputPlaceholder()}
                            
                        >
                            <TranslateButton
                            onClick={translateTextInput}
                            />
                        </TextArea>
                        
                    </div>

                    <div className="" style={{
                        margin:"1rem",
                    }}/>
                    <div className="pargraph-output-text-container">
                        <OutputText
                            onOutputTextChange={onOutputTextChange}
                            text={outputText || ""}
                            placeholder={outputTextPlaceholder}
                            loading={isLoading}
                        />
                    </div>
                </div>

            </div>
        </div>
    )
};
export default ParagraphItem;