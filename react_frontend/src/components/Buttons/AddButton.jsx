import AddIcon from '@mui/icons-material/Add';
import { IconButton } from "@mui/material";
import Fab from '@mui/material/Fab';

export default function AddButton({className, onClick}){
    return (
        <div className= {className}>
            <Fab size="large" color="primary" aria-label="add">
                <AddIcon fontSize="large" onClick={onClick}/>
            </Fab>
        </div>
    );
}