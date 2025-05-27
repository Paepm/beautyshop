import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { logoutUser } from '../services/auth';
import { AuthContext } from '../contexts/AuthContext';

function LogoutButton() {
    const { refreshAuth } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await logoutUser();           // backend logout request
            await refreshAuth();          // AuthContext refresh
            navigate('/');                // than back to home
        } catch (error) {
            console.error("Logout failed", error);
        }
    };

    return (
        <button onClick={handleLogout}>
            Logout
        </button>
    );
}

export default LogoutButton;
