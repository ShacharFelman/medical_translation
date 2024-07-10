import React, { useContext } from 'react';
import LogoTitle from './LogoTitle.jsx';
import Card from './CardLeafletHistory.jsx';
import { TranslateContext } from '../store/TranslateContext.jsx';

function LeafletsHistory({ leaflets }) {
  // const {leafletsCards} = useContext(TranslateContext); 
  return (
    <aside className="w-1/4 bg-gray-100 p-4 overflow-y-auto ">
      <LogoTitle />
      <h2 className="text-xl text-center font-bold mb-8">Leaflets History</h2>
      <div className="space-y-4">
        {leaflets.map(leaflet => (
        <Card 
          key={leaflet.id} 
          name={leaflet.name} 
          date={leaflet.date} 
        />
        ))}
      </div>
    </aside>
  );
}

export default LeafletsHistory;
