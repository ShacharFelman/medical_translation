import {useState, useContext} from 'react';
import TextField from '@mui/material/TextField';
import EditIcon from '@mui/icons-material/Edit';
import CheckIcon from '@mui/icons-material/Check';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import { translteContext } from '../store/TranslateContext.jsx';


export default function LeafletsName() {
    const [isEditing, setIsEditing] = useState(false);
    const { currentLeafletName, handleLeafletNameChange } = useContext(translteContext);

    function handleEdit() {
        setIsEditing(editing => !editing);
        if(isEditing){
            handleLeafletNameChange(currentLeafletName);
        }
    }

    function handleChange(event){
        handleLeafletNameChange(event.target.value);
    }
    
    let editableLefletName= 
        <span >
             <TextField
                disabled = {!isEditing}
                id="outlined-required"
                label="leaflet Name"
                value={currentLeafletName}
                onChange={handleChange}
                variant="outlined"
                className="w-64"
                InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton onClick={handleEdit}>
                        {isEditing ? <CheckIcon fontSize='medium'/> : <EditIcon/>}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
            />  
        </span>
  return (
    <li className="flex justify-center p-4">
        <div className="flex items-center">

        <span className="flex">
            {editableLefletName}
        </span>
        <button
            onClick={handleEdit}
            className=" ml-4 p-2 text-custom-blue rounded hover:text-blue-300 focus:outline-none"
        >
        </button>
        </div>
    </li>
  );
}

