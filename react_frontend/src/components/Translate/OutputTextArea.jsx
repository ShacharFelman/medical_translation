export default function OutputTextArea({translation}){
    return (
      <div className="flex flex-col flex-grow space-y-2">
        <textarea 
          className="rounded-md border p-2 w-full h-56 text-black bg-gray-200" 
          type="text" 
          value={translation} 
          placeholder='Translated Text Here...'
          readOnly 
        /> 
      </div>
      );
}