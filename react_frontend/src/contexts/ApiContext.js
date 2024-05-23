import React, { createContext, useState, useContext, useEffect } from 'react';
import client from '../api/api-client';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useLanguage } from './LanguageContext';

const ApiContext = createContext();

export const ApiProvider = ({ children }) => {
    const {language} = useLanguage();
    const [referenceToken,setReferenceToken] = useState(null);
    const [isServerOnline,setIsServerOnline] = useState(true);
    const [isAppLoading,setIsAppLoading] = useState(true);
    
    const handleResponse = (response) => {
        try{
            if("message" in response){
                toast.success(
                    language._get_text_by_language(response.message),{
                    position:"bottom-right",
                    autoClose:3000
                })
            }else if ("error" in response){
                toast.error(
                    language._get_text_by_language(response.error),{
                    position:"bottom-right",
                    autoClose:10000
                })
            }else if ("data" in response){
                return response.data;
            }
        }catch(error){
            console.error("invalid response format")
        }
        return null;
    }

    useEffect(() => {
        const checkServerStatus = async () => {
            setIsAppLoading(true);
            const response = await client.ping();
            handleResponse(response)
            if(response){
                setIsServerOnline(true)
            }else{
                setIsServerOnline(false)
            }
            setIsAppLoading(false);
        }
        checkServerStatus();
    },[])


    const translateParagraph = async (source,dest,textInput,htmlInput) => {
        const response = await client.translateParagraph(referenceToken,source,dest,textInput,htmlInput);
        return handleResponse(response);
    }

    const downloadDocFile = async (htmlInput) => {
        const blob = await client.downloadDocFile(htmlInput);
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');   
        link.href = url;
        const currentDateTime = new Date().toISOString().replace(/:/g, '-').replace(/\..+/, '');
        const filename = `generated_document_${currentDateTime}.docx`;          
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    const uploadReferenceFile = async (file) => {
        const response = await client.uploadReferenceFile(file);
        if (response.ok){
            const res = await response.json()
            const data = res.data;
            const token = data.reference_token
            if (token){
                setReferenceToken(token);
            }
            toast.success(language.successfullReferenceUploadText(),{
                autoClose:300,
                position:"bottom-right"
            })            
        }
        



        
    }


  
    return (
      <ApiContext.Provider value={{
            referenceToken,
            client,
            translateParagraph,
            uploadReferenceFile,
            isServerOnline,
            isAppLoading,
            downloadDocFile

       }}>
        {children}
      </ApiContext.Provider>
    );
  };
  
export const useApi = () => useContext(ApiContext);