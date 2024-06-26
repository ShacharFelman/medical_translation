import { useLanguage } from "../../contexts/LanguageContext";
import { useTheme } from "../../contexts/ThemeContext";
import AppLogo from "../logo";
import "./header.css"

import il from "../../assets/IL.svg";
import us from "../../assets/US.svg";

const AppHeader = () => {
    const {language,changeLanguage} = useLanguage();
    const headerText = language.headerText();
    const {theme} = useTheme();

    const onIsraelClick = () => {
        changeLanguage({
            title:"heb",
            rtl:true
        })
    }

    const onUSAClick = () => {
        changeLanguage({
            title:"eng",
            rlt:false
        })
    }

    const padding = {
        
    }
    return (
        <div className="header-container" style={{
            backgroundColor:theme.colors.primary,
            color:theme.colors.primaryText,
            maxHeight:"15%",
        }}>
            <div className="logo-header-container" style={{
                
            }}>
                <AppLogo/>
            </div>

            <div className='header' style={{
                // padding:30,
                
            }}>
                    {headerText}
            </div>
            
            <div className="header-right-side" style={{
                
            }}>
                <div className="flag-image-button-container">
                    <img className="flag-image-button"
                        onClick={onUSAClick}
                        alt="English"
                        src={us}
                        />
                </div>

                <div className="flags-seperator" style={{
                    ...theme.components.other,
                }}/>

                <div className="flag-image-button-container">
                    <img className="flag-image-button"
                            onClick={onIsraelClick}
                            alt="Hebrew"
                            src={il}
                        />
                </div>

            </div>
        </div>

    )
}

export default AppHeader;