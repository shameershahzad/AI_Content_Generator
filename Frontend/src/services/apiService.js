import axios from "axios";

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

export const generatePost = async(topic,platform) => {
    const {data} = await api.post('/generate',{topic,platform});
    return data.content;
}