import axios from 'axios';

// const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
const API_BASE_URL = 'http://127.0.0.1:8000';


const API = axios.create({
  baseURL: API_BASE_URL
});

export default async function translateParagraph(source, dest, textInput) {
  const body = {
      source: source,
      dest: dest,
      textInput: textInput
  };
  
  try {
      const response = await API.post('/text', body);
      return response.data.data;
  } catch (error) {
      console.error('Error translating paragraph:', error);
      throw error;
  }
};

export async function saveLeafletToDB(leaflet) {
  try {
    const response = await API.post('/save-leaflet', leaflet);
    return response.data;
  } catch (error) {
    console.error('Error saving leaflet:', error);
    throw error;
  }
}

