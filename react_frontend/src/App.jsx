import { useState } from 'react';
import Header from './components/Header.jsx';
import TranslateSection from './components/TranslationSection.jsx';
import AddButton from './components/Buttons/AddButton.jsx';
import DownloadFileButton from './components/Buttons/DownloadFileButton.jsx';
import LeafletsName from './components/LeafletsName.jsx';
import SaveButton from './components/Buttons/SaveButton.jsx';
import LeafletsHistory from './components/LeafletsHistory.jsx';
import {TranslateContext} from './store/TranslateContext.jsx';
// import TranslateContextProvider from './store/TranslateContext.jsx';

function App() {
  const [sections, setSections] = useState([{id:0}]);
  const [currentLeafletName, setCurrentLeafletName] = useState('Untitle');
  const [leafletsCards, setleafletsCards] = useState([
      { id: 1, name: currentLeafletName, date: '2024-07-01' },
      { id: 2, name: 'Leaflet 2', date: '2024-06-30' },
      // Add more cards as needed
  ]);

  function saveLeaflet() {
      setleafletsCards([...leafletsCards, 
      { id: leafletsCards.length, name: 'Leaflet ' + (leafletsCards.length + 1), date: new Date().toISOString().split('T')[0] }]);
      //save to json file and send to backend to save to database
  }

  function handleLeafletNameChange(newName){
      setCurrentLeafletName(newName);
  }


  function getTranslation(text) {
      return "English: "+ currentLeafletName +" " + text;
  }

  function handleAddSection() {
      const newId = sections.length > 0 ? sections[sections.length - 1].id + 1 : 0;
      setSections([...sections, { id: newId }]);
  }

  function handleDeleteSection(id) {
      sections.length === 1 ? setSections([{id:0}]) :
      setSections(sections.filter(section => section.id !== id));
  }

  const translateCtx = {
      // sections,
      currentLeafletName,
      //lefletsCards :leafletsCards.items  (chnage the name of the items),
      // saveLeaflet,
      setCurrentLeafletName,
      handleLeafletNameChange,
      // getTranslation,
      handleAddSection,
      // handleDeleteSection
  }

  return (
    <TranslateContext.Provider value={{translateCtx}}>
      <div className="flex h-screen">
        <LeafletsHistory leaflets={leafletsCards} />
        <div className="flex flex-col flex-grow">
          <Header />
          <div className="flex justify-center items-center p-4">
            <LeafletsName/>
            <SaveButton title="Save leaflet" />
            <DownloadFileButton />
          </div>
          <main className="flex-grow p-7 flex flex-col">
            {sections.map(section => (
              <TranslateSection key={section.id} getTranslation={getTranslation} onDelete={() => handleDeleteSection(section.id)} />
            ))}
            <AddButton className="flex justify-center p-8" onClick={handleAddSection} />
          </main>
        </div>
      </div>
    </TranslateContext.Provider>
  );
}

export default App;
