import { useState } from 'react';
import Header from './components/Header.jsx';
import DownloadFileButton from './components/Buttons/DownloadFileButton.jsx';
import LeafletsName from './components/LeafletsName.jsx';
import SaveButton from './components/Buttons/SaveButton.jsx';
import LeafletsHistory from './components/History/LeafletsHistory.jsx';
import Leaflet from './components/Translate/Leaflet.jsx';
import TranslateContextProvider from './store/TranslateContext.jsx';

function App() {
  return (
    <TranslateContextProvider>
      <div className="flex h-screen">
        <LeafletsHistory/>
        <div className="flex flex-col flex-grow">
          <Header />
          <div className="flex justify-center items-center p-4">
            <LeafletsName/>
            <SaveButton/>
            <DownloadFileButton />
          </div>
          <Leaflet/>  
        </div>
      </div>
    </TranslateContextProvider>
  );
}

export default App;
