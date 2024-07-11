import {useState, useContext} from 'react';
import TextField from '@mui/material/TextField';
import EditIcon from '@mui/icons-material/Edit';
import CheckIcon from '@mui/icons-material/Check';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import { TranslateContext } from '../store/TranslateContext.jsx';


export default function LeafletsName() {
    const { currentLeafletName, handleLeafletNameChange } = useContext(TranslateContext);
    const [leafletName, setLefletName] = useState(currentLeafletName);
    const [isEditing, setIsEditing] = useState(false);

    function handleEdit() {
        setIsEditing(editing => !editing);
        if(isEditing){
            handleLeafletNameChange(leafletName);
        }
    }

    function handleChange(event){
        setLefletName(event.target.value);
    }
    
    let editableLefletName= 
        <span className="flex">
             <TextField
                disabled = {!isEditing}
                id="outlined-required"
                label="leaflet Name"
                value={leafletName}
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
            {editableLefletName}
            <button
                onClick={handleEdit}
                className=" ml-4 p-2 text-custom-blue rounded hover:text-blue-300 focus:outline-none">
            </button>
        </div>
    </li>
  );
}
