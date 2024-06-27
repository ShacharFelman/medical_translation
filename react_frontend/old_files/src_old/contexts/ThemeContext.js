import React, { createContext, useContext, useState } from 'react';
import { lightStyles } from '../style/theme';

const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
    const [theme, setTheme] = useState({
          title: "Default Theme",
          colors: {
            background: "white",
            primary: "#0D0630",
            secondary: "#7a99bc",
            primaryText: "#F2F7FA",
            text: "#222222",
            buttonBackground: "#34568b",
            buttonText: "#ffffff",
            error: "#cc3333",
            success: "#6ba833",
            warning: "#ffcc33",
            info: "#6699cc"
          },
          typography: {
            default:{
              fontFamily: "font-family: Arial, sans-serif",
              fontSize: "1rem",
            },
          },
          components: {
            dropdown:{
              backgroundColor:"white",
              color: "black",
            },
            other:{
              backgroundColor:"#13C17C"
            },
            part:{
              backgroundColor:"#E8F9F2"
            },
            button: {
              primary:{
                backgroundColor: "#13C17C",
                color: "",
                hoverBackground: "",
                hoverColor: ""
              },
              alt_primary:{
                backgroundColor: "#02B9F3",
                color: "black",
                // hoverBackground: "",
                // hoverColor: ""
              },              
              secondary:{
                backgroundColor: "",
                color: "",
                hoverBackground: "",
                hoverColor: ""
              },  
              alt_secondary:{
                backgroundColor: "#E6F8FE",
                color: "#02B9F3",
                hoverBackground: "",
                hoverColor: ""
              },                            
              alt_secondary_green:{
                backgroundColor: "#E8F9F2",
                color: "#13C17C",
                hoverBackground: "",
                hoverColor: ""
              },          
            },
            input: {
              inputText:{
                fontSize:20,
              },
              outputText:{

              },
              output:{
                backgroundColor:"#F3F7F9",
                
              },
              outputPlaceholder:{
                
              },
              input:{
                fontSize:"1rem"
              },
              inputPlaceholder:{

              },
              backgroundColor: "",
              borderColor: "",
              color: "",
              placeholderColor: ""
            }
          }
}
    );

    return (
      <ThemeContext.Provider value={{
        theme
       }}>
        {children}
      </ThemeContext.Provider>
    );
  };
  
export const useTheme = () => useContext(ThemeContext);