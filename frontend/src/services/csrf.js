// src/services/csrf.js
import api from './api';
import Cookies from 'js-cookie';

export async function ensureCsrfCookie() {
    const token = Cookies.get('csrftoken');
    if (!token) {
        try {
            await api.get('accounts/get-csrf/'); // oder irgendeine sichere Route
            console.log('CSRF cookie successfully loaded');
        } catch (error) {
            console.error('CSRF cookie could not be loaded');
        }
    }
}
