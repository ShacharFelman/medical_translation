import "./add-button.css";
import AddIcon from '@mui/icons-material/Add';
import { IconButton } from "@mui/material";
import { useTheme } from "../../../../../../contexts/ThemeContext";

const AddButton = ({onClick}) => {
    const {theme} = useTheme();
    return (
        <div className="add-button-container">
            <IconButton onClick={onClick}>
                <AddIcon  style={{
                    padding:"0.7rem",
                    fontSize:"2rem",
                    borderRadius:"2rem",
                    ...theme.components.button.alt_secondary,
                }}/>
            </IconButton>
        </div>
    )
}
export default AddButton;