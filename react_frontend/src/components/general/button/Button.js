import { IconButton } from "@mui/material";
import "./button.css";

const Button = ({icon,title="", onClick}) => {
    return (
        <IconButton className="custom-button" onClick={onClick}>
            {icon ? icon : title}
        </IconButton>

    )
}
export default Button;