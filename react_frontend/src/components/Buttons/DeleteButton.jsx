import { IconButton } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';

export default function DeleteButton({onClick}){
    return (
        <div className="flex items-start">
            <IconButton aria-label="delete" color="primary" onClick={onClick}>
                <DeleteIcon/>
            </IconButton>
        </div>
    );
}