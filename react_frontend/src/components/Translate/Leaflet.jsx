import { useContext } from 'react';
import TranslateSection from './TranslationSection.jsx';
import AddButton from '../Buttons/AddButton.jsx';
import LanguageSelection from './LanguageSelection.jsx';
import { TranslateContext } from '../../store/TranslateContext.jsx';

export default function Leaflet() {
    const { currentLeaflet ,
            addSection,
            deleteSection,
            changeInputText,
            updateOutputText 
        } = useContext(TranslateContext);

    // const currentLeaflet = getCurrentLeaflet();

    if (!currentLeaflet) {
        return <div>No leaflet selected</div>;
    }

    return (
        <main className="flex-grow p-7 flex flex-col">
            <LanguageSelection/>
            {currentLeaflet.sections.map(section => (
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