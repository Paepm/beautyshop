import React from 'react';
import { useNavigate } from 'react-router-dom';

import { logoutUser } from '../services/auth';
import { useAuth } from '../contexts/AuthContext';


function LogoutButton() {
    const navigate = useNavigate();
    const { setIsAuthenticated } = useAuth();

    const handleLogout = async () => {
        try {
            await logoutUser();
            setIsAuthenticated(false); // Update the authentication state to not authenticated
            navigate('/'); // to the / page after logout
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    return (
        <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
            Logout
        </button>
    );
}

export default LogoutButton;
