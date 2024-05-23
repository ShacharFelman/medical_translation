import { Box, Tab, Tabs, Typography } from "@mui/material";
import "./tabs.css";

const AppTabs = ({value,onChange,options}) => {
    

    const handleOnChange = (event,value) => {
        onChange(value);
    }

    const getTitleStyle = (index) => {
        return { 
            color:value == index ? "#286267": "",
            textTransform: 'none', 
            fontFamily: '',
            fontSize: "1.7vh"
        }
    }

    const getIconStyle = (index) => {
        return {
            color:value == index ? "#286210": "",
            height:"5vh",
            width:"5vw",

        }
    }
    const boxStyles = {
        // borderBottom: 1, 
        // borderColor: 'divider' ,
        
   }

    return (
        <div className="app-tabs-container">
            <Box sx={boxStyles}>
                <Tabs value={value} onChange={handleOnChange}
                style={{


                }}
                    TabIndicatorProps={{
                        style: {
                        backgroundColor: '#286267',
                        height: "0.5vh",
                        },
                    }}
                    >
                    {options.map((option,index)=>{
                        return (
                            <Tab
                                key={`tab_${option.title}`}
                                label={<Typography variant="button" style={getTitleStyle(index)}>{option.title}</Typography>}
                                icon={option.icon(getIconStyle(index))}
                                style={option?.style}
                                
                            />
                        )
                    })}
                </Tabs>
            </Box>
        </div>
    )
}

export default AppTabs;