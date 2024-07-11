import React, {createContext, useState} from 'react';

export const TranslateContext = createContext();

export default function TranslateContextProvider({children}) {

    const [currentLeafletName, setCurrentLeafletName] = useState('Untitled Leaflet');
    const [sections, setSections] = useState([{ id: 0, inputText: '', translation: '' }]);
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

    function handleAddSection() {
        const newId = sections.length > 0 ? sections[sections.length - 1].id + 1 : 0;
        setSections([...sections, { id: newId, inputText: '', translation: '' }]);
    }
  
    function handleDeleteSection(id) {
        sections.length === 1 ? 
        setSections([{ id: 0, inputText: '', translation: '' }]) :
        setSections(sections.filter(section => section.id !== id));
    }

    function handleInputTextChange(id, newText) {
        setSections(sections.map(section =>
            section.id === id ? { ...section, inputText: newText } : section
        ));
    }

    function handleTranslation(id, newTranslation) {
        setSections(sections.map(section =>
            section.id === id ? { ...section, translation: newTranslation } : section
        ));
    }

    const translateCtx = {
        currentLeafletName,
        sections,
        leafletsCards,
        saveLeaflet,
        handleLeafletNameChange,
        getTranslation,
        addSection: handleAddSection,
        deleteSection: handleDeleteSection,
        changeInputText: handleInputTextChange,
        updateOutputText: handleTranslation
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