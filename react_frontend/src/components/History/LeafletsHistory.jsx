import React, { useContext } from 'react';
import LogoTitle from '../LogoTitle.jsx';
import Card from './CardLeafletHistory.jsx';
import { TranslateContext } from '../../store/TranslateContext';

function LeafletsHistory() {
  const {leafletsCards} = useContext(TranslateContext); 
  return (
    <aside className="w-1/4 bg-gray-100 p-4 overflow-y-auto ">
      <LogoTitle />
      <h2 className="text-xl text-center font-bold mb-8">Leaflets History</h2>
      {leafletsCards.length === 0 ? (
        <p className="text-center text-gray-500">There Is No History Yet</p>
      ) : (
        <div className="space-y-4">
          {leafletsCards.map(leaflet => (
          <Card 
            key={leaflet.id} 
            name={leaflet.name} 
            date={leaflet.date} 
          />
          ))}
        </div>
      )}
    </aside>
  );
}

export default LeafletsHistory;
