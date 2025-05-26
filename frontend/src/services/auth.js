import api from './api';
import Cookies from 'js-cookie';

export async function logoutUser() {
    const csrftoken = Cookies.get('csrftoken');
    return api.post('/accounts/logout/', {}, {
        headers: {
            'X-CSRFToken': csrftoken,
        },
    });
}
