export default function SaveButton({ title, saveLeaflet ,...props}){
    return (
        <button 
            className="px-8 py-4 font-semibold rounded text-gray-100 hover:text-gray-700 bg-custom-blue hover:bg-blue-300"
            // onClick={ saveLeaflet } 
            {...props}
            >{title}
        </button>
    );
}