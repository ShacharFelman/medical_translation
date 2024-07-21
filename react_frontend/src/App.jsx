// import React, { useContext } from 'react';
// import Header from './components/Header.jsx';
// import DownloadFileButton from './components/Buttons/DownloadFileButton.jsx';
// import LeafletName from './components/LeafletName.jsx';
// import SaveButton from './components/Buttons/SaveButton.jsx';
// import LeafletsHistory from './components/History/LeafletsHistory.jsx';
// import Leaflet from './components/Translate/Leaflet.jsx';
// import TranslateContextProvider, { TranslateContext } from './store/TranslateContext.jsx';

// function AppContent() {
//   const { addLeaflet, getCurrentLeaflet } = useContext(TranslateContext);
//   const currentLeaflet = getCurrentLeaflet();

//   return (
//     <div className="flex h-screen">
//       <LeafletsHistory />
//       <div className="flex flex-col flex-grow">
//         <Header />
//         <div className="flex justify-center items-center p-4">
//           {currentLeaflet && <LeafletName />}
//           <SaveButton />
//           <DownloadFileButton />
//           <button 
//             onClick={addLeaflet} 
//             className="ml-4 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
//           >
//             New Leaflet
//           </button>
//         </div>
//         <Leaflet />
//       </div>
//     </div>
//   );
// }

// function App() {
//   return (
//     <TranslateContextProvider>
//       <AppContent />
//     </TranslateContextProvider>
//   );
// }

// export default App;

import React, { useContext } from 'react';
import Header from './components/Header.jsx';
import DownloadFileButton from './components/Buttons/DownloadFileButton.jsx';
import LeafletName from './components/LeafletName.jsx';
import SaveButton from './components/Buttons/SaveButton.jsx';
import LeafletsHistory from './components/History/LeafletsHistory.jsx';
import Leaflet from './components/Translate/Leaflet.jsx';
import TranslateContextProvider, { TranslateContext } from './store/TranslateContext.jsx';

function AppContent() {
  const { currentLeaflet } = useContext(TranslateContext);

  return (
    <div className="flex h-screen">
      <LeafletsHistory />
      <div className="flex flex-col flex-grow">
        <Header />
        <div className="flex justify-center items-center p-4">
          {currentLeaflet && <LeafletName />}
          <SaveButton />
          <DownloadFileButton />
        </div>
        {currentLeaflet ? <Leaflet /> : <p>No leaflet selected. Click "Add New Leaflet" to start.</p>}
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