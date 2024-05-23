import React from 'react'
import "./logo.css"
import image from "../../assets/icon.png";
import { useTheme } from '../../contexts/ThemeContext';

const AppLogo = () => {
    const {theme} = useTheme()
    const onLogoClick = () => {
        window.location.href = '/';
    }

    return (
        <div className="logo-container"  style={{
            display:"flex",
            flexDirection:"row",
            height:"100%",
            alignItems:"center"
        }}>
            <div style={{
                height:"80%"
            }}>
                <img onClick={onLogoClick} className="logo-image" src={image} alt='Icon'  style={{
                    aspectRatio:1,
                    


                    
                }}/>
            </div>


            <div className="flags-seperator" style={{
                    ...theme.components.other,
                    height:"50%"
            }}/>  
            <div style={{
                display:"flex",
                flexDirection:"column",
                justifyContent:"center",
                
            }}>
                
                <div style={{
                    // fontFamiliy: "A"
                    fontFamily:""
                }}>
                    Meditranslate
                </div>
                <div style={{
                    fontFamiliy: "ABeeZee"
                }}>
                    AI
                </div>                  
            </div>          
          
        </div>
    )
}


export default AppLogo;