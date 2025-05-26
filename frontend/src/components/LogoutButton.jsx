import { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import api from '../services/api';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';

function LogoutButton() {
    const { setIsAuthenticated } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            const csrftoken = Cookies.get('csrftoken');

            await api.post('/accounts/logout/', {}, {
                headers: {
                    'X-CSRFToken': csrftoken,
                },
            });

            setIsAuthenticated(false);
            navigate('/');
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    return (
        <button onClick={handleLogout} className="text-red-600 hover:underline">
            Logout
        </button>
    );
}

export default LogoutButton;
