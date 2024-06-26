
import { useLanguage } from "../../../../../../contexts/LanguageContext";
import { useTheme } from "../../../../../../contexts/ThemeContext";
import "./table-of-content.css";

const ParagraphsTableOfContent = ({currentParagraphIndex,textInputs,onParagraphHeaderClick}) => {
    const {isRTL, language} = useLanguage();
    const {theme} = useTheme()
    const partLabel = language.partText();

    return (
        <div className="table-content-container" style={{
            direction:"rtl",
            overflowY:"scroll",
            height:"100%",
            width:"100%",
        }}>
            {textInputs.map((_,index) => {
                return (
                    <div key={`table-content-header-number_${index}`} className="table-content-header" onClick={() => onParagraphHeaderClick(index)} style={
                        currentParagraphIndex === index ? {
                            ...theme.components.part,
                            fontWeight:"bold",
                            fontSize:"1.2rem"
                        } : {
                            fontWeight:"bold",
                            fontSize:"1.2rem",                            
                            opacity:0.5
                        }
                    }>
                           {isRTL ?`${partLabel} ${index + 1}`: `${partLabel} ${index + 1} ` } 
                    </div>
                )
            })}
        </div>
    )
}

export default ParagraphsTableOfContent;