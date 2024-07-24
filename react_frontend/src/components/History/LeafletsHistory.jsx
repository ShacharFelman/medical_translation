// import React, { useContext } from 'react';
// import LogoTitle from '../LogoTitle.jsx';
// import LeafletHistoryCard from './LeafletHistoryCard.jsx';
// import { TranslateContext } from '../../store/TranslateContext';

// function LeafletsHistory() {
//   const { leaflets } = useContext(TranslateContext); 

//   return (
//     <aside className="w-1/4 bg-gray-100 p-4 overflow-y-auto">
//       <LogoTitle />
//       <h2 className="text-xl text-center font-bold mb-8">Leaflets History</h2>
//       {leaflets.length === 0 ? (
//         <p className="text-center text-gray-500">There Is No History Yet</p>
//       ) : (
//         <div className="space-y-4">
//           {leaflets.map((leaflet) => (
//             <LeafletHistoryCard 
//               key={leaflet.id} 
//               leaflet={leaflet} />
//           ))}
//         </div>
//       )}
//     </aside>
//   );
// }

// export default LeafletsHistory;

import React, { useContext } from 'react';
import LogoTitle from '../LogoTitle.jsx';
import LeafletHistoryCard from './LeafletHistoryCard.jsx';
import { TranslateContext } from '../../store/TranslateContext';

function LeafletsHistory() {
  const { leaflets, addNewLeaflet } = useContext(TranslateContext); 

  return (
    <aside className="w-1/4 bg-gray-100 p-4 overflow-y-auto">
      <LogoTitle />
      <button 
        onClick={addNewLeaflet} 
        className="w-full mb-4 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
      >
        Add New Leaflet
      </button>
      <h2 className="text-xl text-center font-bold mb-8">Leaflets History</h2>
      {leaflets.length === 0 ? (
        <p className="text-center text-gray-500">There Is No History Yet</p>
      ) : (
        <div className="space-y-4">
          {leaflets.map((leaflet) => (
            <LeafletHistoryCard key={leaflet.id} leaflet={leaflet} />
          ))}
        </div>
      )}
    </aside>
  );
}

export default LeafletsHistory;