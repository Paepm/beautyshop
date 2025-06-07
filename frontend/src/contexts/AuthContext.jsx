import { createContext, useEffect, useState } from 'react';
import api from '../services/api';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchUser = async () => {
        try {
            const response = await api.get('/accounts/me/');
            console.log('Authenticated user:', response.data);
            setIsAuthenticated(true);
            setUser(response.data);
        } catch (error) {
            if (error.response?.status === 401) {
                console.warn('User is not authenticated:', error.response.data);
            } else {
                console.error('Error fetching user:', error);
            }
            setIsAuthenticated(false);
            setUser(null);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUser();
    }, []);

    return (
        <AuthContext.Provider value={{
            isAuthenticated,
            setIsAuthenticated,
            user,
            refreshAuth: fetchUser,
            loading,
        }}>
            {children}
        </AuthContext.Provider>
    );
}
