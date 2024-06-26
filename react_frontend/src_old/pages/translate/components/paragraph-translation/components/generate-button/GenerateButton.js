import { useLanguage } from "../../../../../../contexts/LanguageContext";
import { useTheme } from "../../../../../../contexts/ThemeContext";
import "./generate-button.css";
const GenerateButton = ({disabled,onClick}) => {
    const {language} = useLanguage()
    const title = language.generateText();
    const {theme} = useTheme();
    
    const disabledStyles = {
        ...theme.components.button.primary,
        opacity:0.5
    }

    const activeStyles = {
        ...theme.components.button.primary
    }

    return (
            <button 
                className="generate-button" 
                style={disabled ? disabledStyles : activeStyles} 
                disabled={disabled} 
                onClick={onClick}
            >
                {title}
            </button>
    )
}
export default GenerateButton;