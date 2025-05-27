import axios from 'axios';

const api = axios.create({
    baseURL: '/api/',
    withCredentials: true,  // for the sessionid cookie from Django backend
});

export default api;