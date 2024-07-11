import React, {createContext, useState, useReducer} from 'react';

export const TranslateContext = createContext();

function translateReducer(leafletState, action) {
  switch (action.type) {
    case 'ADD_SECTION':
      const newId = leafletState.sections.length > 0 ? leafletState.sections[leafletState.sections.length - 1].id + 1 : 0;
      return {
        ...leafletState,
        sections: [...leafletState.sections, { id: newId, inputText: '', translation: '' }]
      };
    case 'DELETE_SECTION':
      return {
        ...leafletState,
        sections: leafletState.sections.length === 1 
          ? [{ id: 0, inputText: '', translation: '' }] 
          : leafletState.sections.filter(section => section.id !== action.id)
      };

    case 'CHANGE_INPUT_TEXT':
      return {
        ...leafletState,
        sections: leafletState.sections.map(section =>
          section.id === action.id ? { ...section, inputText: action.newText } : section
        )
      };
    case 'UPDATE_OUTPUT_TEXT':
      return {
        ...leafletState,
        sections: leafletState.sections.map(section =>
          section.id === action.id ? { ...section, translation: action.newTranslation } : section
        )
      };
    default:
      return leafletState;
  }
}


export default function TranslateContextProvider({children}) {
    const initialState = { sections: [{ id: 0, inputText: '', translation: '' }] };
    const [leafletState, leafletDispatch] = useReducer(translateReducer, initialState);
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

    const addSection = () => {
      leafletDispatch({ type: 'ADD_SECTION' });
    };
  
    const deleteSection = (id) => {
      leafletDispatch({ type: 'DELETE_SECTION', id });
    };
  
    const changeInputText = (id, newText) => {
      leafletDispatch({ type: 'CHANGE_INPUT_TEXT', id, newText });
    };
  
    const updateOutputText = (id, newTranslation) => {
      leafletDispatch({ type: 'UPDATE_OUTPUT_TEXT', id, newTranslation });
    };

    const translateCtx = {
        currentLeafletName,
        sections: leafletState.sections,
        leafletsCards,
        saveLeaflet,
        handleLeafletNameChange,
        getTranslation,
        addSection,
        deleteSection,
        changeInputText,
        updateOutputText
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