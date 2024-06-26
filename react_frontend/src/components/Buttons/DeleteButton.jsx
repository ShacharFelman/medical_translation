import { IconButton } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';

export default function DeleteButton({onClick}){
    return (
        <IconButton aria-label="delete" color="primary" >
            <DeleteIcon onClick={onClick}/>
        </IconButton>
    );
}