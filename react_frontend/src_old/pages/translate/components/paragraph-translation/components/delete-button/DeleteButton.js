import "./delete-button.css";
import { IconButton } from "@mui/material";
import DeleteOutlineOutlinedIcon from '@mui/icons-material/DeleteOutlineOutlined';
import CloseIcon from '@mui/icons-material/Close';
import { useLanguage } from "../../../../../../contexts/LanguageContext";

const DeleteButton = ({onDelete,deleteable}) => {
    const handleOnDelete = () => {
        if(deleteable){
            onDelete()   
        }
    }
    return (
        <div className="paragraph-list-item-delete-button-container">
            <IconButton style={{
                opacity:0.8,   
                paddingTop:"1rem",
                paddingLeft:"2rem",
                paddingRight:"2rem",
                color:"red"
                
            }} onClick={handleOnDelete}>
                <DeleteOutlineOutlinedIcon style={{
                    width:"1.5rem",
                    height:"1.5rem",
                }}/> 
            </IconButton>
        </div>  
    )
}

export default DeleteButton;