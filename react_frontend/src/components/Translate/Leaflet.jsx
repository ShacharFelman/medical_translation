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

    if (!currentLeaflet) {
        return <div>No leaflet selected</div>;
    }

    return (
        <main className="flex p-4 flex-col h-full">
            <LanguageSelection/>
            <div className="flex-grow overflow-y-auto">
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
            </div>
            <AddButton className="flex justify-center flex-shrink-0" onClick={addSection} />
      </main>
    );
}