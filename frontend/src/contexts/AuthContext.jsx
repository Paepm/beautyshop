import { createContext, useEffect, useState } from 'react';
import api from '../services/api';

// Create the context job
export const AuthContext = createContext();

// Export the provider as Wrapper-component
export function AuthProvider({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await api.get('/accounts/me/');
                console.log('Authenticated user:', response.data);
                setIsAuthenticated(true);
            } catch (error) {
                console.warn('Not logged in:', error.response?.status);
                setIsAuthenticated(false);
            } finally {
                setLoading(false);
            }
        };

        fetchUser();
    }, []);

    if (loading) return <div>Loading...</div>;

    return (
        <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated }}>
            {children}
        </AuthContext.Provider>
    );
}
