import React, { useContext } from 'react';
import Header from './components/Header.jsx';
import DownloadFileButton from './components/Buttons/DownloadFileButton.jsx';
import LeafletName from './components/LeafletName.jsx';
import SaveButton from './components/Buttons/SaveButton.jsx';
import LeafletsHistory from './components/History/LeafletsHistory.jsx';
import Leaflet from './components/Translate/Leaflet.jsx';
import TranslateContextProvider, { TranslateContext } from './store/TranslateContext.jsx';
import ErrorMessage from './components/ErrorMessage.jsx';


function AppContent() {
  const { currentLeaflet } = useContext(TranslateContext);

  return (
    <div className="flex h-screen overflow-hidden">
      <div className="w-1/4 flex-shrink-0">
        <LeafletsHistory />
      </div>
      <div className="w-3/4 flex flex-col overflow-hidden">
        <Header />
        <div className="px-4 py-2">
          <ErrorMessage />
        </div>
        <div className="flex justify-center items-center p-4">
          {currentLeaflet && <LeafletName />}
          <SaveButton />
          <DownloadFileButton />
        </div>
        <div className="flex-grow overflow-y-auto">
          {currentLeaflet ? <Leaflet /> : <p className="text-center mt-8">No leaflet selected. Click "Add New Leaflet" to start.</p>}
        </div>      
      </div>
    </div>
  );
}

function App() {
  return (
    <TranslateContextProvider>
      <AppContent />
    </TranslateContextProvider>
  );
}

export default App;