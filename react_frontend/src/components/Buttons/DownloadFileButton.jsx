import React, { useContext } from 'react';
import DownloadIcon from '@mui/icons-material/Download';
import { IconButton } from "@mui/material";
import { TranslateContext } from '../../store/TranslateContext';

export default function DownloadFileButton(){
    const {downloadDocFile} = useContext(TranslateContext);
    return (
        <div className="ml-4">
            <IconButton 
                size="large" 
                color="primary" 
                aria-label="add"
                onClick={downloadDocFile}>
                <DownloadIcon fontSize='large' />
            </IconButton>
        </div>
    );
}
