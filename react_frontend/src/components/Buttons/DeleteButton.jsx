import { IconButton } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';

export default function DeleteButton({onClick, className}){
    return (
        <div className={className}>
            <IconButton aria-label="delete" color="primary" onClick={onClick}>
                <DeleteIcon/>
            </IconButton>
        </div>
    );
}