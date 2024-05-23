import { useLanguage } from "../../../../../../contexts/LanguageContext";
import { useTheme } from "../../../../../../contexts/ThemeContext";
import "./translate-button.css";

const TranslateButton = ({onClick}) => {
    const {language} = useLanguage()
    const {theme} = useTheme()
    return (
        <div className="translate-button-container" onClick={onClick} style={{
            // backgroundColor:"orange",
            // borderRadius:30,
            // padding:"1vh",
            // paddingLeft:"1.5vw",
            // paddingRight:"1.5vw",  
            ...theme.components.button.primary

        }}>
           {language.translateText()}
        </div>
    )

}

export default TranslateButton;