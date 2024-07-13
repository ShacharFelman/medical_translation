import Dropdown from "../../components/general/dropdown";
import { useLanguage } from "../../contexts/LanguageContext";
import "./settings-page.css";

const appLanguages = [

    {
        label:"english",
        value:"eng"
    },
    {
        label:"עברית",
        value:"heb"
    },

]

const SettingsPage = () => {
    const {language,getLanguage,changeLanguage} = useLanguage();
    
    const handleOnLanguageChange = (value) => {
        changeLanguage(value);
    }

    return (
        <div style={{
            // margin:"5%",
            borderColor:"lightgray",
            borderWidth:1,
            borderStyle: "solid",
            borderRadius:5,
            padding:5,
            flex:1,
            position:"absolute",
            width:"80%",
            // transform: "translate(-50%, -50%)"
            height:"60%",
            top: "60%",
            left: "50%",
            transform: "translate(-50%, -50%)"


            // backgroundColor:"red",
        }}>
            <div style={{
                textAlign:"center",
                
            }}>
                <div style={{
                    marginBottom:20,
                    fontSize:25,
                }}>
                    {language.languageText()}
                </div>
                <div>
                    <Dropdown
                        value={getLanguage()}
                        options={appLanguages}
                        onChange={handleOnLanguageChange}
                    /> 
                </div>
            </div>


        </div>
    )
}

export default SettingsPage;