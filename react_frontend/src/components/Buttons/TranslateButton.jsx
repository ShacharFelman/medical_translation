export default function TranslateButton({ title, ...props}){
    return (
        <button 
            className="px-4 py-2 font-semibold rounded text-gray-100 hover:text-gray-700 bg-custom-blue hover:bg-blue-300" 
            // className="px-4 py-2 font-semibold rounded text-stone-900 bg-blue-300 hover:bg-cyan-200" 
            {...props}
            >{title}
        </button>
    );
}