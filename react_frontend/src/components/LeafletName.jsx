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

// import { useState, useContext, useEffect } from 'react';
// import TextField from '@mui/material/TextField';
// import EditIcon from '@mui/icons-material/Edit';
// import CheckIcon from '@mui/icons-material/Check';
// import InputAdornment from '@mui/material/InputAdornment';
// import IconButton from '@mui/material/IconButton';
// import { TranslateContext } from '../store/TranslateContext.jsx';

// export default function LeafletName() {
//     const { currentLeaflet, handleLeafletNameChange } = useContext(TranslateContext);
//     const [leafletName, setLeafletName] = useState('');
//     const [isEditing, setIsEditing] = useState(false);

//     useEffect(() => {
//         // const currentLeaflet = getCurrentLeaflet();
//         if (currentLeaflet) {
//             setLeafletName(currentLeaflet.name);
//         }
//     }, [currentLeaflet]);

//     function handleEdit() {
//         setIsEditing(editing => !editing);
//         if (isEditing) {
//             handleLeafletNameChange(leafletName);
//         }
//     }

//     function handleChange(event) {
//         setLeafletName(event.target.value);
//     }
    
//     if (!currentLeaflet) {
//         return null;
//     }

//     return (
//         <li className="flex justify-center p-4">
//             <div className="flex items-center">
//                 <TextField
//                     disabled={!isEditing}
//                     id="outlined-required"
//                     label="Leaflet Name"
//                     value={leafletName}
//                     onChange={handleChange}
//                     variant="outlined"
//                     className="w-64"
//                     InputProps={{
//                         endAdornment: (
//                             <InputAdornment position="end">
//                                 <IconButton onClick={handleEdit}>
//                                     {/* {isEditing ? "Save" : <EditIcon/>} */}
//                                     {isEditing ? <CheckIcon fontSize='medium'/> : <EditIcon/>}
//                                 </IconButton>
//                             </InputAdornment>
//                         ),
//                     }}
//                 />
//             </div>
//         </li>
//     );
// }

