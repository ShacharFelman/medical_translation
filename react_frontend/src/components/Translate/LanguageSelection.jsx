export default function LanguageSelection() {
    return (
        <div className="flex justify-between w-full mb-4 space-x-4">
            <select className="rounded-md border p-2 w-[49%] h-10 bg-white text-black">
                <option>English</option>
            </select>  
            <select className="rounded-md border p-2 w-[49%] h-10 bg-white text-black">                
                <option>Hebrew</option>
            </select>      
        </div>
    );
}
// w-[45%]