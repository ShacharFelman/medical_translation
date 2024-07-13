import { useEffect, useRef, useState } from "react";
import "./paragraph-translation.css";

import { toast } from "react-toastify";
import { useApi } from "../../../../contexts/ApiContext";
import ParagraphList from "./components/paragraph/list/ParagraphList";
import GenerateButton from "./components/generate-button";
import LanguagesPickers from "../../../../components/languages-pickers";
import AddButton from "./components/add-button/AddButton";
import DownloadButton from "./components/download-button";
import ToastWarningContinueModal from "./components/toast-warning-continue-modal/ToastWarningContinueModal";
import { useLanguage } from "../../../../contexts/LanguageContext";
import ParagraphsTableOfContent from "./components/table-of-content/ParagraphsTableOfContent";
import OutputText from "../../../../components/output-text";



const ParagraphTranslation = () => {
    const {translateParagraph,referenceToken} = useApi();
    const {language} = useLanguage();
    const [isAllFinishLoading,setIsAllFinishLoading] = useState(true);
    const [currentParagraphIndex, setCurrentParagraphIndex ] = useState(0);
    const [modalPresented,setModalPresented] = useState(false);    
    const [textInputs, setTextInputs] = useState([{
        input:"",
        loading:false,
        output:null,
        rawtext:""
    }]); 

    const buttonDisabled = false;//referenceToken === null;

    const sourceLanguageOptions = [
        {
            label:language.hebrewText(),
            value:"heb"
        },
    ]
    
    const destLanguageOptions = [
        {
            label:language.englishText(),
            value:"eng"
        },
    
    ]
    const [sourceLanguage,setSourceLanguage] = useState(sourceLanguageOptions[0].value);
    const [destLanguage,setDestLanguage] = useState(destLanguageOptions[0].value);

    const currentTextInputs = useRef(textInputs)


    const handleOnSourceLanChange = (value) => {
        setSourceLanguage(value);
    }
    const handleOnDestLanChange = (value) => {
        setDestLanguage(value)
    }

    // const onLanguageSwap = () => {
    //     const isAllowSource = sourceLanguageOptions.map((i)=>i.value).includes(destLanguage);
    //     const isAllowDest = destLanguageOptions.map((i)=>i.value).includes(sourceLanguage);
    //     if(isAllowDest && isAllowDest){
    //         const tempSourceLanguage = sourceLanguage;
    //         const tempDestLanguage = destLanguage;
    //         setSourceLanguage(tempDestLanguage);
    //         setDestLanguage(tempSourceLanguage);
    //         return;
    //     }
    //     let errorText = "";
    //     if (!isAllowDest){
    //         errorText += `${destLanguage} unsupported as source language. \n`;
    //     }
    //     if (!isAllowSource){
    //         errorText += !isAllowDest ? "and " : "";
    //         errorText += `${sourceLanguage} unsupported as destination language. \n`;
    //     }
    //     toast.error(errorText,{
    //         autoClose:10000,
    //     })
    // }


    const onAddParagraph = () => {
        const newParagraphs = [...textInputs,{
            input:"",
            rawtext:"",
            loading:false,
            output:null
        }];
        setTextInputs(newParagraphs);
    }

    const onParagraphDelete = (index) => {
        const newParagraphs = [...textInputs];
        if (newParagraphs.length > 1){
            newParagraphs.splice(index, 1);    
        }        
        setTextInputs(newParagraphs);
    }



    const onTextChange = (index,value,text) =>{
        const newItems = textInputs.map((item,t_index)=>{
            if (index === t_index){
                return {
                    input:value,
                    rawtext:text,
                    loading:item.loading,
                    output:item.output
                }
            }
            return item;
        })
        setTextInputs(newItems);
    }
    useEffect(()=>{
        currentTextInputs.current = textInputs
    },[textInputs])


    const onOutputTextChange = (index,text) =>{
        const newItems = textInputs.map((item,t_index)=>{
            if (index === t_index){
                return {
                    output:text,
                    rawtext:item.rawtext,
                    loading:item.loading,
                    input:item.input
                }
            }
            return item;
        })
        setTextInputs(newItems);
    }


    const onClear = (index) =>{
        const newItems = textInputs.map((item,t_index)=>{
            if (index === t_index){
                return {
                    output:"",
                    loading:false,
                    input:"",
                    rawtext:""
                }
            }
            return item;
        })
        setTextInputs(newItems);
    }

    

    const translateTextInput = async (index,multiple=false) => {
        if(multiple){
            if(textInputs[index].input.trim().length === 0){
                return;
            }            
            const invalidError = getInvalidError(textInputs[index].input)
            if(invalidError !== null){
                toast.error(
                    language._get_text_by_language(invalidError),{
                    autoClose:1000,
                })
                const itemId = getParagraphItemIdByIndex(index)
                scrollToItem(itemId);
                return false;
            }
    
        }

        setTextInputs(prevTextInputs => {
            return prevTextInputs.map((item, t_index) => {
                if (index === t_index) {
                    return {
                        input: item.input,
                        loading: true,
                        output: item.output,
                        rawtext: item.rawtext
                    };
                }
                return item;
            });
        });

        

        const output = await translateParagraph(
            sourceLanguage,
            destLanguage,
            textInputs[index].rawtext,
            textInputs[index].input,
            

        );
        console.log("one:",output)
        

        setTextInputs(prevTextInputs => {
            return prevTextInputs.map((item, t_index) => {
                if (index === t_index) {
                    return {
                        input: item.input,
                        loading: false,
                        output: output,
                        rawtext:item.rawtext
                    };
                }
                return item;
            });
        });           
        console.log("two:",output)
        return output   
    }
    


    function getInvalidError(textInput){
        if (!(/[\u0590-\u05FF]/).test(textInput)){
            return {
                "heb":"text does not contains hebrew",
                "eng":"text does not contains hebrew"
            }
        }
        return null
    }

    const translate = () => {
        let isInput = false;
        if(textInputs.map((item,index)=>{
            if(item.input.trim().length > 0){
                isInput = true
            }else{
                const itemId = getParagraphItemIdByIndex(index)
                scrollToItem(itemId);
            }
        }))
        if(!isInput){
            toast.error(language.pleaseEnterTextText(),{
                autoClose:1000,
            })
            return;
        }

        translateTextInputs();
    }

    useEffect(() => {
        console.log("effects:",textInputs)
    }, [textInputs])
    const translateTextInputs = async () => {
        setIsAllFinishLoading(false);
        const outputs = await Promise.all(textInputs.map(async (text, index) => {
            return await translateTextInput(index,true);
        }));
        console.log("outputs:", outputs)
        
        setTextInputs(prevTextInputs => {
            return prevTextInputs.map((item, index) => {
                return {
                    input: item.input,
                    loading: false,
                    output: outputs[index],
                    rawtext:item.rawtext
                };
            });
        });
        
        setIsAllFinishLoading(true);
    }





    const getParagraphItemIdByIndex = (index) => {
        const itemId = `paragraph_number_${index}`
        return itemId
    }

    const onParagraphHeaderClick = (index) => {
        const itemId = getParagraphItemIdByIndex(index)
        scrollToItem(itemId);
        setCurrentParagraphIndex(index);
    }

    const scrollToItem = (itemId) => {
        const itemElement = document.getElementById(`${itemId}`);
        if (itemElement) {
          itemElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      };

      


      useEffect(()=>{
        const targetSections = document.querySelectorAll("[id*='paragraph_number_']");
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                  const paraga = entry.target.getAttribute("id").split("paragraph_number_")
                  if(paraga && paraga[1]){
                    setCurrentParagraphIndex(parseInt(paraga[1]))
                  }
                }
              });
          },{
            threshold:0.7
          });
          targetSections.forEach((section) => {
            observer.observe(section);
          });                  
      },[textInputs])

    return (
        <div className="input-output-paragraph-translation-option-container">
            {true && 
                (
                    <DownloadButton 
                        textInputs={textInputs}
                    />
                )
            }               
            <div style={{
                display:"flex",
                overflowY:"hidden",
                flex:5,
                maxHeight:"55vh"
                
            }}>


                <div style={{
                        display:"flex",
                        flex:1,
                        flexDirection:"row",
                        justifyContent:"flex-start",
                        maxHeight:"100%"
                        
                }}>
                    <div className="page-table-of-content-container" style={{
                        
                    }}>
                        <ParagraphsTableOfContent 
                            currentParagraphIndex={currentParagraphIndex}
                            textInputs={textInputs}
                            onParagraphHeaderClick={onParagraphHeaderClick}
                        />   
                    </div>                
                    <div style={{
                        flex:1,
                        display:"flex",
                        flexDirection:"column",
                        marginLeft:"5rem"
                    }}> 
                        <div style={{
                            marginRight:"5.5rem",
                            flex:1,
                            
                        }}>
                        <LanguagesPickers
                                destLanguage={destLanguage}
                                destLanguageOptions={destLanguageOptions}
                                handleOnDestLanChange={handleOnDestLanChange}
                                handleOnSourceLanChange={handleOnSourceLanChange}
                                sourceLanguage={sourceLanguage}
                                sourceLanguageOptions={sourceLanguageOptions}
                        />
                        </div>
  
                        <div style={{
                            marginBottom:"1rem",
                        }}/>
                        <div className="page-paragraph-list-container" style={{
                            flex: 10,
                            display: "flex",
                            flexDirection:"column",
                            overflowY:"auto",

                        }}>
                            <ParagraphList 
                                textInputs={textInputs}
                                setTextInputs={setTextInputs}
                                onDelete={onParagraphDelete}
                                onTextChange={onTextChange}
                                onOutputTextChange={onOutputTextChange}
                                onClear={onClear}
                                translateTextInput={translateTextInput}  
                            />   
                        </div>
                            
                    </div>

                
                </div>
            </div>

 
            <div style={{
                display:"flex",
                flex:1,
                flexDirection:"column",
                
            }}>
                <div style={{
                    
                    display:"flex",
                    flexDirection:"row",
                    flex:1,
                    
                }}>
                    <div style={{
                        
                        display:"flex",
                        flex:1
                    }}>

                    </div>
                    <div style={{
                        display:"flex",
                        flex:1,
                        justifyContent:"center",
                        alignItems:"center",
                        
                        
                    }}>
                        <div style={{
                            
                            display:"flex",
                        }}>
                            <GenerateButton 
                                disabled={buttonDisabled}
                                onClick={translate}
                            />
                        </div>


                    </div>

                    <div style={{
                        flex:1,
                        display:"flex",
                        
                        
                    }}>
                        <div style={{
                            flex:1,
                        }}>
                            <AddButton onClick={onAddParagraph}/>
                        </div>
                        

                    </div>

                </div>
        
            </div>

        </div>
    )
}

export default ParagraphTranslation;
