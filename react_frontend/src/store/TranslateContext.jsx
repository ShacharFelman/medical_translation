import React, {createContext, useState} from 'react';

export const TranslateContext = createContext();

export default function TranslateContextProvider({children}) {

    const [currentLeafletName, setCurrentLeafletName] = useState('Untitled Leaflet');

    const [leafletsCards, setLeafletsCards] = useState([
      { id: 1, name: currentLeafletName, date: '2024-07-01' },
      { id: 2, name: 'Leaflet 2', date: '2024-06-30' },
      // Add more cards as needed
    ]);
  
    const saveLeaflet = () => {
      setLeafletsCards([...leafletsCards, 
        { id: leafletsCards.length + 1, name: `Leaflet ${leafletsCards.length + 1}`, date: new Date().toISOString().split('T')[0] }
      ]);
      // Save to JSON file and send to backend to save to database
    };
  
    const handleLeafletNameChange = (newName) => {
      setCurrentLeafletName(newName);
    };
  
    const getTranslation = (text) => {
        return `English: ${currentLeafletName} ${text}`;
    };

    const translateCtx = {
        currentLeafletName,
        leafletsCards,
        saveLeaflet,
        handleLeafletNameChange,
        getTranslation
    };

    return (
        <TranslateContext.Provider value={translateCtx}>
           {children}
        </TranslateContext.Provider>
    );
}


// const translateParagraph = async (source,dest,textInput,htmlInput) => {
//     const response = await client.translateParagraph(referenceToken,source,dest,textInput,htmlInput);
//     return handleResponse(response);
// }