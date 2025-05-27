import api from './api';
import Cookies from 'js-cookie';

export async function logoutUser() {
    const csrftoken = Cookies.get('csrftoken');
    return api.post('/accounts/logout/', {}, {
        headers: {
            'X-CSRFToken': csrftoken,
        },
        withCredentials: true, // Ensure cookies are sent with the request
    });
}

/**
 * Sends a login request to the backend with credentials.
 *
 * @param {string} username_or_email - The username or email entered by the user.
 * @param {string} password - The password entered by the user.
 * @returns {Promise} Axios response from the backend
 */

export async function loginUser(username_or_email, password) {
    const csrftoken = Cookies.get('csrftoken');
    return api.post('/accounts/login/', {
        username_or_email,
        password
    }, {
        headers: {
            'X-CSRFToken': csrftoken,
        },
        withCredentials: true, // Ensure cookies are sent with the request
    });
}
