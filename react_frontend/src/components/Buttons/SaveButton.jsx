import React, { useContext } from 'react';
import { TranslateContext } from '../../store/TranslateContext';

export default function SaveButton() {
  const { saveLeaflet } = useContext(TranslateContext);
    return (
        <button 
            className="px-8 py-4 font-semibold rounded text-gray-100 hover:text-gray-700 bg-custom-blue hover:bg-blue-300"
            onClick={ saveLeaflet } 
            >Save Leaflet
        </button>
    );
}