export default function LanguageSelection() {
    return (
        <div className="flex flex-grow space-x-5">
            <select className="rounded-md border p-2 w-full h-10 bg-white text-black">
                <option>English</option>
            </select>  
            <select className="rounded-md border p-2 w-full h-10 bg-white text-black">
                <option>Hebrew</option>
            </select>      
        </div>
    );
}
