import React from 'react';

export default function CardLeafletHistory({ name, date }) {
  return (
    <div className="border border-gray-300 shadow-lg rounded-lg p-4 bg-white m-2">
      <h2 className="text-lg font-bold">{name}</h2>
      <p className="text-gray-600">{date}</p>
    </div>
  );
}

