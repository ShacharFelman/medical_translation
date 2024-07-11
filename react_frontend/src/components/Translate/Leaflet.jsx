import { useState, useContext } from 'react';
import TranslateSection from './TranslationSection.jsx';
import AddButton from '../Buttons/AddButton.jsx';
import LanguageSelection from './LanguageSelection.jsx';
import { TranslateContext } from '../../store/TranslateContext.jsx';

export default function Leaflet() {
    const { getTranslation } = useContext(TranslateContext);
    const [sections, setSections] = useState([{ id: 0, inputText: '', translation: '' }]);

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

    return (
        <main className="flex-grow p-7 flex flex-col">
            <LanguageSelection/>
            {sections.map(section => (
                <TranslateSection 
                    key={section.id}
                    inputText={section.inputText}
                    translation={section.translation} 
                    getTranslation={getTranslation} 
                    onDelete={() => handleDeleteSection(section.id)} 
                    onInputChange={(newText) => handleInputTextChange(section.id, newText)}
                    onTranslate={(newTranslation) => handleTranslation(section.id, newTranslation)}
                />
            ))}
            <AddButton className="flex justify-center p-8" onClick={handleAddSection} />
      </main>
    );
}