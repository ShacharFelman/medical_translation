import React from 'react';
import LoadingLogo from '../loadingLogo/LoadingLogo';

export default function OutputTextArea({translation, isTranslating}) {
    return (
      <div className="flex flex-col flex-grow space-y-2 w-2/12">
         {isTranslating ? (
        <div className="rounded-md border p-2 w-full h-56 flex items-center justify-center bg-gray-200">
          <LoadingLogo />
        </div>
      ) : (
        <div className="rounded-md border w-full h-56 bg-gray-200 overflow-hidden">
          <div 
            className="w-full h-full p-2 overflow-y-auto text-black
                      [&_h1]:font-bold [&_h1]:underline [&_h1]:text-xl
                      [&_h2]:font-bold [&_h2]:text-lg
                      [&_ul]:list-disc [&_ul]:pl-5
                      [&_ol]:list-decimal [&_ol]:pl-5
                      [&_li]:my-1"
            dangerouslySetInnerHTML={{ __html: translation }}
          />
        </div>
      )}
      </div>
    );
}