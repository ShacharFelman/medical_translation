import config from "../config/config"

class ApiClient {
    constructor() {
        if (!ApiClient.instance) {
            this.base_url = config.server_url;
            ApiClient.instance = this;
        }

        return ApiClient.instance;
    }

    async _request_file(path, method, body = null, headers = null) {
        const defaultHeaders = {
            "content-type":"application/json"
        }
        const requestOptions = {
            method: method
        };
        if (headers){
            requestOptions['headers'] = headers;
        }else{
            requestOptions['headers'] = defaultHeaders;
            
        }
        if (body){
            requestOptions['body'] = JSON.stringify(body);
            
        }        
        
        try {
            const response = await fetch(this.base_url + path, requestOptions);
            return response;
        } catch (error) {
            console.error(error)
        }
    }

    async _request(path, method, body = null, headers = null) {
        const defaultHeaders = {
            "content-type":"application/json"
        }
        const requestOptions = {
            method: method
        };
        if (headers){
            requestOptions['headers'] = headers;
        }else{
            requestOptions['headers'] = defaultHeaders;
            
        }
        if (body){
            requestOptions['body'] = JSON.stringify(body);
            
        }        
        
        try {
            const response = await fetch(this.base_url + path, requestOptions);
            const jsonData = await response.json();
            return jsonData;
        } catch (error) {
            console.error(error)
        }
    }

    async ping(){
        const response = await this._request("/api/ping","GET");
        return response;
    }


    async uploadReferenceFile(file){   
        const formData = new FormData();
        formData.append('file', file);
        const response = await fetch(this.base_url + "/reference", {
            method:"POST",
            body: formData 
        });
        return response
    }

    async translateParagraph(referenceToken,source,dest,textInput,htmlInput){
        const formData = new FormData();
        formData.append('referenceToken', referenceToken);
        formData.append('source', source);
        formData.append('dest', dest);
        formData.append('textInput', textInput);
        formData.append('htmlInput', htmlInput);

        
        const body = {
            referenceToken: referenceToken,
            source:source,
            dest:dest,
            textInput: textInput,
            htmlInput: htmlInput
        }
        const response =  await this._request("/text","POST",body,null);
        return response;
    }

    async downloadDocFile(htmlInput){
        const body = {
            htmlInput: htmlInput
        }
        const response =  await this._request_file("/html-docx","POST",body,null);
        if (!response.ok) {
            
        }
        const file = await response.blob()
        return file;        
    }

}

const instance = new ApiClient();
Object.freeze(instance);

export default instance;
