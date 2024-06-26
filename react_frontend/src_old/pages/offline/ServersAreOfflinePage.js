import LanguageIcon from '@mui/icons-material/Language';
import "./offline-page.css";

const ServersAreOfflinePages = () => {
    return (
        <div className="offline-container">
        <div className="offline-content">
          <h1>Oops!</h1>
          <p>It seems like you're offline.</p>
          <p>Please check your internet connection and try again.</p>
          <LanguageIcon/>
        </div>
      </div>
    )
}

export default ServersAreOfflinePages;