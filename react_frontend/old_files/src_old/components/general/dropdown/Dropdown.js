import { MenuItem, Select } from "@mui/material";
import "./dropdown.css"
import { useTheme } from "../../../contexts/ThemeContext";

const Dropdown = ({value,options,onChange}) => {
    const {theme} = useTheme();
    const handleOnChange = (event) => {
        onChange(event.target.value);
    }

    return (     
            <Select
            className='dropdown-select'
            value={value}
            label="Language"
            onChange={handleOnChange}
            style={{
                color:"#286267",
                backgroundColor:"white",
                fontSize:"1.2rem",
                maxHeight:"2.4rem",
                fontWeight:"bold",
                ...theme.components.dropdown
            }}
        >
            {options.map((op)=>{
                return (
                    <MenuItem 
                    key={`${op.label}_${op.value}`}

                    style={ 
                        op.value === value ?
                        {
                            justifyContent:"center",
                            fontWeight:"bold"
                        }:{
                        }}
                    value={op.value}>{op.label}</MenuItem>
                )
            })}
        </Select>
    )
}

export default Dropdown;

