import { useContext, useEffect, useState } from 'react';
import TextField from '@mui/material/TextField';
import { TranslateContext } from '../store/TranslateContext.jsx';

export default function LeafletName() {
    const { currentLeaflet, handleLeafletNameChange } = useContext(TranslateContext);
    const [leafletName, setLeafletName] = useState('');

    useEffect(() => {
        if (currentLeaflet) {
            setLeafletName(currentLeaflet.name);
        }
    }, [currentLeaflet]);

    function handleChange(event) {
        const newName = event.target.value;
        setLeafletName(newName);
        handleLeafletNameChange(newName);
    }
    
    if (!currentLeaflet) {
        return null;
    }

    return (
        <li className="flex justify-center p-4">
            <div className="flex items-center">
                <TextField
                    id="leaflet-name"
                    label="Leaflet Name"
                    value={leafletName}
                    onChange={handleChange}
                    variant="outlined"
                    className="w-64"
                />
            </div>
        </li>
    );
}
