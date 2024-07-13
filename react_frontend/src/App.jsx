import { useState } from 'react';
import Header from './components/Header.jsx';
import DownloadFileButton from './components/Buttons/DownloadFileButton.jsx';
import LeafletsName from './components/LeafletsName.jsx';
import SaveButton from './components/Buttons/SaveButton.jsx';
import LeafletsHistory from './components/History/LeafletsHistory.jsx';
import Leaflet from './components/Translate/Leaflet.jsx';
import TranslateContextProvider from './store/TranslateContext.jsx';

function App() {
  const [leafletsCards, setleafletsCards] = useState([
      { id: 1, name: 'Leaflet 1', date: '2024-07-01' },
      { id: 2, name: 'Leaflet 2', date: '2024-06-30' },
      // Add more cards as needed
  ]);

  function saveLeaflet() {
      setleafletsCards([...leafletsCards, 
      { id: leafletsCards.length, name: 'Leaflet ' + (leafletsCards.length + 1), date: new Date().toISOString().split('T')[0] }]);
      //save to json file and send to backend to save to database
  }

  return (
    <TranslateContextProvider>
      <div className="flex h-screen">
        <LeafletsHistory leaflets={leafletsCards} />
        <div className="flex flex-col flex-grow">
          <Header />
          <div className="flex justify-center items-center p-4">
            <LeafletsName/>
            <SaveButton title="Save leaflet" />
            <DownloadFileButton />
          </div>
          <Leaflet/>  
        </div>
      </div>
    </TranslateContextProvider>
  );
}

export default App;
