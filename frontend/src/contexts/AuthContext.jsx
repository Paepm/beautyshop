import { createContext, useEffect, useState } from 'react';
import api from '../services/api';

// Create the context job
export const AuthContext = createContext();

// Export the provider as Wrapper-component
export function AuthProvider({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);


    const fetchUser = async () => {
        try {
            const response = await api.get('/accounts/me/');
            console.log('Authenticated user:', response.data);
            setIsAuthenticated(true);
        } catch (error) {
            if (error.response?.status === 401) {
                // User is not authenticated
                console.warn('User is not authenticated:', error.response.data);
            } else {
                // Other errors
                console.error('Error fetching user:', error);
            }
            console.warn('Not logged in:', error.response?.status);
            setIsAuthenticated(false);
        } finally {
            setLoading(false);
        }
    }


    useEffect(() => {
        fetchUser();
    }, []);

    return (
        <AuthContext.Provider value={{
            isAuthenticated,
            setIsAuthenticated,
            refreshAuth: fetchUser,
            loading // <-- neu!
        }}>
            {children}
        </AuthContext.Provider>
    );
}

