// This file sets up an Axios instance for making API requests to the Django backend.
// It configures the base URL and enables credentials for session management.
// The base URL is set to '/api/' which should match the Django API endpoint.
// The 'withCredentials' option is set to true to allow cookies (like sessionid) to be sent with requests.
import axios from 'axios';
import Cookies from 'js-cookie';

const api = axios.create({
    baseURL: '/api/',
    withCredentials: true,  // for the sessionid cookie from Django backend
});
console.log("Axios baseURL:", api.defaults.baseURL);



api.interceptors.request.use((config) => {
    const method = config.method?.toLowerCase();
    const needsCsrf = ["post", "put", "patch", "delete"].includes(method);

    if (needsCsrf) {
        const token = Cookies.get("csrftoken");
        if (token) {
            config.headers["X-CSRFToken"] = token;
        }
    }
    return config;
});

export default api;

