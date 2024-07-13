import "./fileviewer.css"

const FileViewer = ({fileUrl}) => {
    return (
        <div className="file-viewer-container">
            <iframe src={fileUrl} title="File Viewer" ></iframe>
        </div>
    )
}

export default FileViewer;