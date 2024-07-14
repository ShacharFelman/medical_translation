import React, {createContext, useState, useReducer, useEffect} from 'react';
import translateParagraph , {saveLeafletToDB, fetchLeafletsFromDB } from '../api/Api';

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
    case 'SET_LEAFLET_NAME':
      return {
        ...leafletState,
        name: action.name
      };  
    default:
      return leafletState;
  }
}

export default function TranslateContextProvider({children}) {
    const initialState = { sections: [{ id: 0, inputText: '', translation: '' }], name: 'Untitled Leaflet' };
    const [leafletState, leafletDispatch] = useReducer(translateReducer, initialState);
    const [leafletsCards, setLeafletsCards] = useState([]);
  
    const fetchLeaflets = async () => {
      try {
          // const fetchedLeaflets = await fetchLeafletsFromDB();
          // console.log('Fetched leaflets:', fetchedLeaflets);
          // setLeafletsCards(fetchedLeaflets);
      } catch (error) {
          console.error('Error fetching leaflets:', error);
      }
    };

    useEffect(() => {
      fetchLeaflets();
    }, []);

    const saveLeaflet = async () => {
      const leafletToSave  = {
        name: leafletState.name,
        date: new Date().toISOString(),
        sections: leafletState.sections
      };

       // Log the data of the sections that should be saved
       console.log('Saving leaflet with the following data:');
       console.log('Leaflet Name:', leafletToSave.name);
       console.log('Sections:');
       leafletToSave.sections.forEach((section, index) => {
         console.log(`Section ${index + 1}:`);
         console.log('  ID:', section.id);
         console.log('  Input Text:', section.inputText);
         console.log('  Translation:', section.translation);
       });
      
      try {
        // await saveLeafletToDB(leafletToSave );
        const newCard = { id: leafletsCards.length + 1, name: leafletToSave.name, date: leafletToSave.date };
        setLeafletsCards(prevCards => [...prevCards, newCard]);
        // setLeafletsCards([...leafletsCards, newCard]);
        
        // Log the data of the leaflet that was saved
        leafletsCards.forEach((leaflet, index) => {
          console.log('  ID:', leaflet.id);
          console.log('  name:', leaflet.name);
          console.log('  date:', leaflet.date);
        });

        console.log('  Leaflet saved successfully');
      } catch (error) {
        console.error('Error saving leaflet:', error);
      }
    };

    const getTranslation = async(text) => {
      try{
        const translate = await translateParagraph('heb', 'eng', text);
        console.info('***********************Translation:', translate);
        return translate;
      }
      catch(error){
        console.error('Error translating paragraph:', error);
        return 'Error translating paragraph';
      }
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

    const handleLeafletNameChange = (newName) => {
      leafletDispatch({ type: 'SET_LEAFLET_NAME', name: newName })
    };

    const translateCtx = {
        currentLeafletName: leafletState.name,
        sections: leafletState.sections,
        leafletsCards,
        saveLeaflet,
        handleLeafletNameChange,
        getTranslation,
        addSection,
        deleteSection,
        changeInputText,
        updateOutputText,
        fetchLeaflets  
    };

    return (
        <TranslateContext.Provider value={translateCtx}>
           {children}
        </TranslateContext.Provider>
    );
}
