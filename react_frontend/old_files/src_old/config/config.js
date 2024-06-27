class Config {
    constructor(){
        if (!Config.instance) {
            if (process.env.NODE_ENV === "development"){
                this.server_url =  process.env.REACT_APP_API_URL;
            }else{
                this.server_url =  "";
            }
            Config.instance = this;
        }

        return Config.instance;
        
    }
}

const config = new Config();
export default config;