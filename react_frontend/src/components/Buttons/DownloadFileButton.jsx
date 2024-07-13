import DownloadIcon from '@mui/icons-material/Download';
import { IconButton } from "@mui/material";
import Fab from '@mui/material/Fab';

export default function DownloadFileButton({className, onClick}){
    return (
        <div className={className}>
            <IconButton size="large" color="primary" aria-label="add">
                <DownloadIcon />
            </IconButton>
        </div>
    );
}