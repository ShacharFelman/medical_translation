import AddIcon from '@mui/icons-material/Add';
import { IconButton } from "@mui/material";
import Fab from '@mui/material/Fab';

export default function AddButton({className, onClick}){
    return (
        <div className= {className}>
            <Fab size="medium" color="primary" aria-label="add">
                <AddIcon onClick={onClick}/>
            </Fab>
        </div>
    );
}