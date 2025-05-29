// This file sets up an Axios instance for making API requests to the Django backend.
// It configures the base URL and enables credentials for session management.
// The base URL is set to '/api/' which should match the Django API endpoint.
// The 'withCredentials' option is set to true to allow cookies (like sessionid) to be sent with requests.
import axios from 'axios';


const api = axios.create({
    baseURL: '/api/',
    withCredentials: true,  // for the sessionid cookie from Django backend
});
console.log("Axios baseURL:", api.defaults.baseURL);


export default api;