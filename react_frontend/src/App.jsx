import { useState } from 'react';
import Header from './components/Header.jsx';
import TranslateSection from './components/TranslationSection.jsx';
import AddButton from './components/Buttons/AddButton.jsx';
import DownloadFileButton from './components/Buttons/DownloadFileButton.jsx';
function App() {
  const [sections, setSections] = useState([{id:0}]);

  function getTranslation(text) {
    return "English: " + text;
  }

  function handleAddSection() {
    const newId = sections.length > 0 ? sections[sections.length - 1].id + 1 : 0;
    setSections([...sections, { id: newId }]);
  }

  function handleDeleteSection(id) {
    sections.length === 1 ? setSections([{id:0}]) :
    setSections(sections.filter(section => section.id !== id));
  }

  return (
    <div className="flex flex-col">
      <Header />
      <main className="flex-grow">
        <DownloadFileButton className="flex justify-end pr-10 p-1"/>
        {sections.map(section=> (
          <TranslateSection key={section.id} getTranslation={getTranslation} onDelete={() => handleDeleteSection(section.id)} />
        ))}
          <AddButton className="flex justify-center p-8" onClick={handleAddSection}/>
      </main>
      
    </div>
  );
}

export default App;
