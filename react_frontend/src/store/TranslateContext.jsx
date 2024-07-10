import {createContext, useState} from 'react';

export const TranslateContext = createContext({
    currentLeafletName: 'Untitled',
    // sections: []
});

// export default function TranslateContextProvider({children}) {
//     const [sections, setSections] = useState([{id:0}]);
//     const [currentLeafletName, setCurrentLeafletName] = useState('Untitle');
//     const [leafletsCards, setleafletsCards] = useState([
//         { id: 1, name: currentLeafletName, date: '2024-07-01' },
//         { id: 2, name: 'Leaflet 2', date: '2024-06-30' },
//         // Add more cards as needed
//     ]);

//     function saveLeaflet() {
//         setleafletsCards([...leafletsCards, 
//         { id: leafletsCards.length, name: 'Leaflet ' + (leafletsCards.length + 1), date: new Date().toISOString().split('T')[0] }]);
//         //save to json file and send to backend to save to database
//     }

//     function handleLeafletNameChange(newName){
//         setCurrentLeafletName(newName);
//     }


//     function getTranslation(text) {
//         return "English: "+ currentLeafletName +" " + text;
//     }

//     function handleAddSection() {
//         const newId = sections.length > 0 ? sections[sections.length - 1].id + 1 : 0;
//         setSections([...sections, { id: newId }]);
//     }

//     function handleDeleteSection(id) {
//         sections.length === 1 ? setSections([{id:0}]) :
//         setSections(sections.filter(section => section.id !== id));
//     }

//     const translateCtx = {
//         sections,
//         currentLeafletName,
//         leafletsCards,
//         saveLeaflet,
//         setCurrentLeafletName,
//         handleLeafletNameChange,
//         getTranslation,
//         handleAddSection,
//         handleDeleteSection
//     }

//     return (
//         <TranslateContext.Provider value={{translateCtx}}>
//            {children}
//         </TranslateContext.Provider>
//     );
// }




const translateParagraph = async (source,dest,textInput,htmlInput) => {
    const response = await client.translateParagraph(referenceToken,source,dest,textInput,htmlInput);
    return handleResponse(response);
}