import { useContext, useState } from 'react';
import { Alert, AlertTitle, Collapse } from '@mui/material';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { TranslateContext } from '../store/TranslateContext.jsx';

const ErrorMessage = () => {
  const [expanded, setExpanded] = useState(false);
  const { error, clearError } = useContext(TranslateContext);

  if (!error) return null;

  return (
    <Alert 
      severity="error"
      className="mb-4 w-full"
      action={
        <>
          <IconButton
            aria-label="expand"
            color="inherit"
            size="small"
            onClick={() => setExpanded(!expanded)}
          >
            <ExpandMoreIcon />
          </IconButton>
          <IconButton
            aria-label="close"
            color="inherit"
            size="small"
            onClick={clearError}
          >
            <CloseIcon fontSize="inherit" />
          </IconButton>
        </>
      }
    >
      <AlertTitle>Error</AlertTitle>
      {error.message}
      <Collapse in={expanded}>
        <div className="mt-2">
          <p><strong>Error Code:</strong> {error.code}</p>
          <p><strong>Details:</strong> {error.details}</p>
        </div>
      </Collapse>
    </Alert>
  );
};

export default ErrorMessage;