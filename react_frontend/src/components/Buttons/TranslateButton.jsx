export default function TranslateButton({ title, ...props}){
    return (
        <button 
            className="px-4 py-2 font-semibold rounded text-gray-100 hover:text-gray-700 bg-custom-blue hover:bg-blue-300" 
            {...props}
            >{title}
        </button>
    );
}