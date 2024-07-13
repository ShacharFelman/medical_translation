import { useState, useContext } from 'react';
import TranslateSection from './TranslationSection.jsx';
import AddButton from '../Buttons/AddButton.jsx';
import LanguageSelection from './LanguageSelection.jsx';
import { TranslateContext } from '../../store/TranslateContext.jsx';

export default function Leaflet() {
    const { sections ,
            addSection,
            deleteSection,
            changeInputText,
            updateOutputText 
        } = useContext(TranslateContext);

    return (
        <main className="flex-grow p-7 flex flex-col">
            <LanguageSelection/>
            {sections.map(section => (
                <TranslateSection 
                    key={section.id}
                    inputText={section.inputText}
                    translation={section.translation} 
                    onDelete={() =>deleteSection(section.id)} 
                    onInputChange={(newText) => changeInputText(section.id, newText)}
                    onTranslate={(newTranslation) => updateOutputText(section.id, newTranslation)}
                />
            ))}
            <AddButton className="flex justify-center p-8" onClick={addSection} />
      </main>
    );
}