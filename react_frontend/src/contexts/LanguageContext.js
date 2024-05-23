import React, { createContext, useState, useContext, useEffect } from 'react';
import 'react-toastify/dist/ReactToastify.css';
import Language from '../language/Language';
import { readFromStorage, writeToStorage } from '../storage/storage';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
const LanguageContext = createContext();


const hebrew = "heb";
const english = "eng";


export const LanguageProvider = ({ children }) => {
    const [langaugeLoading,setLanguageLoading]=  useState(true);
    const [language,setLanguage] = useState(new Language(english))
    const [isRTL, setIsRTL] = useState(false);

    useEffect(()=>{
      const readLanguageFromStorage = async () => {
        setLanguageLoading(true);
        const initialLanguage = readFromStorage("language")
        if (!initialLanguage){
          writeToStorage("language",english)
          setLanguage(new Language(english));
        }else{
          setLanguage(new Language(initialLanguage))
        }

        if(initialLanguage === hebrew){
          setIsRTL(true);
        }
        setLanguageLoading(false);

      }
      readLanguageFromStorage();
    },[])


    const changeLanguage = (newLan) => {
        writeToStorage("language",newLan.title);
        setIsRTL(newLan.rtl)
        const newLanguageInstance = new Language(newLan.title);
        setLanguage(newLanguageInstance);
    }

    const getLanguage = () => {
      return language.language;
    }
  

    return (
      <LanguageContext.Provider value={{
        langaugeLoading,
        language,
        setLanguage,
        getLanguage,
        changeLanguage,
        isRTL
       }}>
        {children}
      </LanguageContext.Provider>
    );
  };
  
export const useLanguage = () => useContext(LanguageContext);