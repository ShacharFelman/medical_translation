import {useState} from 'react';
import TextField from '@mui/material/TextField';
import EditIcon from '@mui/icons-material/Edit';
import CheckIcon from '@mui/icons-material/Check';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';


export default function LeafletsName({onChangeName}) {
    const [leafletName, setLefletName] = useState("Untitled Leaflet");
    const [isEditing, setIsEditing] = useState(false);

    function handleEdit() {
        setIsEditing(editing => !editing);
        if(isEditing){
            onChangeName(leafletName);
        }
    }

    function handleChange(event){
        setLefletName(event.target.value);
    }
    
    let editableLefletName= 
        <span >
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

        {/* <div className="flex items-center border-custom-blue border-2 p-2 rounded"> */}
    {/* <li className={isActive ? 'active' : undefined}> */}
        <span className="flex">
            {editableLefletName}
        </span>
        <button
            onClick={handleEdit}
            // className="ml-4 p-2 text-gray-200 bg-gray-200 rounded hover:bg-cyan-700 focus:outline-none"
            className=" ml-4 p-2 text-custom-blue rounded hover:text-blue-300 focus:outline-none"
        >
            {/* {isEditing ? <CheckIcon fontSize='medium'/> : <EditIcon/>} */}
        </button>
        {/* <button onClick={handleEdit}>{isEditing ? 'Save' : 'Edit'}</button> */}
        </div>
    </li>
  );
}