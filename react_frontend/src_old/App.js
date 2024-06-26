import React from 'react';
import './App.css';
import { ApiProvider } from "./contexts/ApiContext"
import AppLayout from './layout/AppLayout';
import { ToastContainer } from 'react-toastify';
import { ThemeProvider } from './contexts/ThemeContext';
import { LanguageProvider } from './contexts/LanguageContext';

const App = () => {
  return (
      <LanguageProvider>
        <ThemeProvider>
          <ApiProvider>
            <AppLayout/>
            <ToastContainer />
          </ApiProvider>
        </ThemeProvider>
      </LanguageProvider>
  );
}

export default App;
