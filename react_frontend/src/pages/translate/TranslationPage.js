import "./translation-page.css";
import ParagraphTranslation from "./components/paragraph-translation";
import ReferenceFileUpload from "../../components/reference-file-upload";


const TransationPage = () => {
 
    const renderTranslationPage = () => {
        return <ParagraphTranslation />
    }

    return (
        <div className="translation-page-container" >
            <div style={{
                flex:1,
                display:"flex",
                flexDirection:"column",

            }}>
                <div style={{
                    padding:"3vh",
                }}>
                    <ReferenceFileUpload />
                </div>
                
            </div>
            <div style={{
                flex:4,
                display:"flex",
                flexDirection:"column"
            }}>
                {renderTranslationPage()}
            </div>
        </div>
    )
}
export default TransationPage;