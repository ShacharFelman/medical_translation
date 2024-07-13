import "./layout.css";
import { useState } from "react";
import AppFooter from "./footer/AppFooter";
import AppHeader from "./header/AppHeader";
import TransationPage from "../pages/translate";
import { useLanguage } from "../contexts/LanguageContext";
import LoadingPage from "../pages/LoadingPage";
import { useApi } from "../contexts/ApiContext";
import ServersAreOfflinePage from "../pages/offline/ServersAreOfflinePage";
import { useTheme } from "../contexts/ThemeContext";


const AppLayout = () => {
    const [selectedPage,setSelectedPage] = useState(0);
    const {langaugeLoading,language} = useLanguage();
    const {isServerOnline,isAppLoading} = useApi();
    const {theme} = useTheme();
    

    if(langaugeLoading || isAppLoading){
        return <LoadingPage/>
    }
    if(!isServerOnline){
        return <ServersAreOfflinePage/>
    }
    

    const renderPage = () => {
        let content;
        if (selectedPage === 0) {
            content = <TransationPage /> 
        } else if (selectedPage === 1) {
            // content = <SettingsPage/>
            
        } else if (selectedPage === 2) {
            // content = <MainPage />;
        }
        return content;
    }


    return (
        <div className="website-app-container" style={{
            backgroundColor:theme.colors.background,
            ...theme.typography.default,
            
        }}>
            
            <AppHeader/>
            <div className="app-body-container">
                {renderPage()}
            </div>
            <AppFooter/>
        </div>
    )
}

export default AppLayout;