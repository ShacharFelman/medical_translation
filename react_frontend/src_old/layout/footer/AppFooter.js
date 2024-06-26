import { useTheme } from "../../contexts/ThemeContext";
import "./footer.css"

const currentYear = new Date().getFullYear();
const footerMessage = `
    Copyright © ${currentYear} MeditranslateAI
`

const AppFooter = () => {
    const {theme} = useTheme()
    return (
      <div className='footer' style={{
        backgroundColor:theme.colors.primary,
        color:theme.colors.primaryText,
        maxHeight:"10%",
      }}>
          <div className="footerText">
            {footerMessage}
          </div>
      </div>
    )
  }



export default AppFooter;