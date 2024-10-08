import React, { useContext } from 'react';
import { TranslateContext } from '../../store/TranslateContext';
import { format } from 'date-fns';
import DeleteButton from '../Buttons/DeleteButton';
export default function LeafletHistoryCard({ leaflet }) {
  const { selectLeaflet , currentLeaflet , deleteLeaflet } = useContext(TranslateContext);
  const isSelected = currentLeaflet.id === leaflet.id;

  return (
    <div 
      className={`
        border rounded-lg p-4 bg-white m-2 cursor-pointer
        transition-all duration-200 ease-in-out
        ${isSelected 
          ? 'border-blue-500 border-2 shadow-lg ring-2 ring-blue-300' 
          : 'border-gray-300 hover:bg-gray-100'
        }
      `}
      onClick={() => selectLeaflet(leaflet)}
    >
      <div className=" flex justify-between items-center">
        <div className="flex-grow">
          <h2 className={`text-lg ${isSelected ? 'font-bold' : 'font-semibold'}`}>{leaflet.name}</h2>
          <p className="text-gray-600">{format(new Date(leaflet.date), 'dd/MM/yyyy HH:mm')}</p>
        </div>
        <DeleteButton onClick={()=> deleteLeaflet(leaflet.id)} className= "flex" />
      </div>
    </div>
  );
}