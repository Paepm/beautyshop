import api from './api';

export async function fetchCSRFToken() {
    try {
        console.log('Trying to fetch CSRF token...');
        await api.get('/accounts/get-csrf/');
        console.log('CSRF token requested successfully');
    } catch (error) {
        console.error('Failed to fetch CSRF token:', error);
    }
}
