import { IconButton } from "@mui/material";
import "./download-button.css";
import DownloadIcon from '@mui/icons-material/Download';
import { useTheme } from "../../../../../../contexts/ThemeContext";
import { useApi } from "../../../../../../contexts/ApiContext";

const DownloadButton = ({textInputs}) => {
    const {theme} = useTheme();
    const {downloadDocFile} = useApi()
    const getFormattedDateTime = () => {
        const currentDate = new Date();
        const formattedDate = currentDate.toISOString().split('T')[0];
        const formattedTime = currentDate.toTimeString().split(' ')[0].replace(/:/g, '');
        return `${formattedDate}_${formattedTime}`;
    }


    const onDownloadFileClick = () => {
        const formattedDateTime = getFormattedDateTime();
        const content = generateFileContent(textInputs);
        const parser = new DOMParser();
        const htmlDoc = parser.parseFromString(content, "text/html");
        const body = htmlDoc.body;     
        const htmlString = body.outerHTML;        
        downloadDocFile(htmlString)
      
    }

    const generateFileContent = (inputs) => {
        let alltext = ``;
        inputs.forEach((textInput, index) => {
            alltext += textInput.output + "</br></br>"
        });
        return alltext;
    }



    return (
        <div className="download-button-container" style={{
            
        }}>
            <IconButton onClick={onDownloadFileClick} style={{
                ...theme.components.button.alt_secondary_green,
                border: "1px solid aliceblue"

            }}>
                <DownloadIcon
                    style={{
                        width:"2rem",
                        height:"2rem",
                    }}
                />
            </IconButton>
        </div>
    )
}

export default DownloadButton;