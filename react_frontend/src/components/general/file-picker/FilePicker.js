import AttachFileOutlinedIcon from '@mui/icons-material/AttachFileOutlined';
import { IconButton } from '@mui/material';
import { useLanguage } from '../../../contexts/LanguageContext';



const FilePicker = ({title,file,onChange}) => {
    const {language} = useLanguage();
    const dir = language.getDirection();
    const filePickerId = `file-upload-input-${title}`;
    const handleFileChange = (event) => {
        const file = event.target.files[0];
        onChange(file);
    };
    

    const handleIconClick = () => {
        document.getElementById(filePickerId).click();
    };

    return (
        <div className='filepicker-container' style={{

        }}>
            <label htmlFor="file-upload-input"> 
                    {dir === "rtl" && (
                        <span className="file-name">
                            {file && file.name || language.noFileSelectedText() + " "}
                        </span>   
                    )} 
                    <IconButton component="span" onClick={handleIconClick}>
                        <AttachFileOutlinedIcon />
                    </IconButton>
                    {dir !== "rtl" && (
                        <span className="file-name">
                            {file && file.name || language.noFileSelectedText() + " "}
                        </span>   
                    )}                     
                    {/* <span className="file-name">
                        {file && file.name || language.noFileSelectedText() + " "}
                    </span>           */}
                    <input 
                        className='file-upload-input'
                        id={filePickerId}
                        //accept="pdf/*"
                        type="file" 
                        onChange={handleFileChange} 
                        style={{
                            opacity:0,
                            height:0,
                            width:0,
                        }}
                    />     
            </label>

      </div>        
    )
}

export default FilePicker;