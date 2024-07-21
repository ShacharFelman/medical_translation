import React, { createContext, useReducer, useEffect } from 'react';
import translateParagraph, { saveLeafletToDB, fetchLeafletsFromDB } from '../api/Api';

export const TranslateContext = createContext();

const createNewLeaflet = () => ({
  id: Date.now(),
  name: 'Untitled Leaflet',
  date: new Date().toISOString(),
  sections: [{ id: 0, inputText: '', translation: '' }]
});


function translateReducer(state, action) {
  switch (action.type) {
    case 'SET_LEAFLETS':
      return {
        ...state,
        leaflets: action.leaflets
      };
    case 'NEW_CURRENT_LEAFLET':
      return {
        ...state,
        currentLeaflet: createNewLeaflet()
      };
    case 'SET_CURRENT_LEAFLET':
    return {
      ...state,
      currentLeaflet: {...action.leaflet} 
    };
    case 'UPDATE_CURRENT_LEAFLET':
      return {
        ...state,
        currentLeaflet: { ...state.currentLeaflet, ...action.updates }
      };
    case 'ADD_SECTION':
      return {
        ...state,
        currentLeaflet: {
          ...state.currentLeaflet,
          sections: [
            ...state.currentLeaflet.sections,
            { id: state.currentLeaflet.sections.length, inputText: '', translation: '' }
          ]
        }
      };
    case 'DELETE_SECTION':
      return {
        ...state,
        currentLeaflet: {
          ...state.currentLeaflet,
          sections: state.currentLeaflet.sections.length === 1 
            ? [{ id: 0, inputText: '', translation: '' }] 
            : state.currentLeaflet.sections.filter(section => section.id !== action.sectionId)
        }
      };
    case 'CHANGE_INPUT_TEXT':
      return {
        ...state,
        currentLeaflet: {
          ...state.currentLeaflet,
          sections: state.currentLeaflet.sections.map(section =>
            section.id === action.sectionId ? { ...section, inputText: action.newText } : section
          )
        }
      };
    case 'UPDATE_OUTPUT_TEXT':
      return {
        ...state,
        currentLeaflet: {
          ...state.currentLeaflet,
          sections: state.currentLeaflet.sections.map(section =>
            section.id === action.sectionId ? { ...section, translation: action.newTranslation } : section
          )
        }
      };
    default:
      return state;
  }
}

export default function TranslateContextProvider({children}) {
    const initialState = { 
      leaflets: [],
      currentLeaflet: createNewLeaflet()
    };
    const [state, dispatch] = useReducer(translateReducer, initialState);
  
    const fetchLeaflets = async () => {
      try {
          const fetchedLeaflets = await fetchLeafletsFromDB();
          dispatch({ type: 'SET_LEAFLETS', leaflets: fetchedLeaflets });
      } catch (error) {
          console.error('Error fetching leaflets:', error);
      }
    };

    useEffect(() => {
      fetchLeaflets();
    }, []);

    const saveLeaflet = async () => {
      if (!state.currentLeaflet) return;

      try {
        await saveLeafletToDB(state.currentLeaflet);
        dispatch({ type: 'SET_LEAFLETS', leaflets: [...state.leaflets, state.currentLeaflet] });
        dispatch({ type: 'NEW_CURRENT_LEAFLET' });
        console.log('Leaflet saved successfully');
      } catch (error) {
        console.error('Error saving leaflet:', error);
      }
    };

    const getTranslation = async(text) => {
      try{
        const translate = await translateParagraph('heb', 'eng', text);
        return translate;
      }
      catch(error){
        console.error('Error translating paragraph:', error);
        return 'Error translating paragraph';
      }
    };
    
    const addNewLeaflet = () => {
      dispatch({ type: 'NEW_CURRENT_LEAFLET' });
    };

    const addSection = () => {
      dispatch({ type: 'ADD_SECTION' });
    };
  
    const deleteSection = (sectionId) => {
      dispatch({ type: 'DELETE_SECTION', sectionId });
    };
  
    const changeInputText = (sectionId, newText) => {
      dispatch({ type: 'CHANGE_INPUT_TEXT', sectionId, newText });
    };
  
    const updateOutputText = (sectionId, newTranslation) => {
      dispatch({ type: 'UPDATE_OUTPUT_TEXT', sectionId, newTranslation });
    };

    const handleLeafletNameChange = (newName) => {
      dispatch({ type: 'UPDATE_CURRENT_LEAFLET', updates: { name: newName } });
    };

    const selectLeaflet = (leaflet) => {
      dispatch({ type: 'SET_CURRENT_LEAFLET', leaflet });
    };

    const translateCtx = {
        currentLeaflet: state.currentLeaflet,
        leaflets: state.leaflets,
        saveLeaflet,
        addNewLeaflet,
        selectLeaflet,
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