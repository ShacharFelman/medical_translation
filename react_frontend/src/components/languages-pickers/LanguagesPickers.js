import { IconButton } from "@mui/material";
import "./languages-pickers.css";
import Dropdown from "../general/dropdown";

const LanguagesPickers = ({
    destLanguage,
    destLanguageOptions,
    handleOnDestLanChange,
    onLanguageSwap,
    sourceLanguage,
    sourceLanguageOptions,
    handleOnSourceLanChange
}) => {
    return (
        <div className="languages-picker-div-container">
            <div className="languages-picker-container">
                <div className="langauge-dropdown-container">
                    <Dropdown
                        value={destLanguage}
                        options={destLanguageOptions}
                        onChange={handleOnDestLanChange}
                    />  
                </div>
                <div className="languages-picker-seperator"/>

                <div className="langauge-dropdown-container">
                    <Dropdown
                        value={sourceLanguage}
                        options={sourceLanguageOptions}
                        onChange={handleOnSourceLanChange}
                    />
                </div>
                      
                {/* <div className="swap-button-container">
                    <IconButton onClick={onLanguageSwap}>
                        <SwapHorizOutlinedIcon sx={{fontSize:35}}/>

                    </IconButton>  
                </div> */}

            </div>

        </div>
    )
}

export default LanguagesPickers;