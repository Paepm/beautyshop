import { Link } from 'react-router-dom';

import { useAuth } from '../../contexts/AuthContext';
import LogoutButton from '../LogoutButton';

function Header() {
    const { isAuthenticated } = useAuth();

    return (
        <header className="p-4 shadow bg-white flex justify-between items-center">
            <Link to="/" className="text-2xl font-bold text-gray-800">
                BeautyShop
            </Link>
            <nav className="space-x-4">
                {isAuthenticated ? (
                    <>
                        <LogoutButton />
                        <Link to="/profile">Profil</Link>
                    </>
                ) : (
                    <>
                        <Link to="/login">Login</Link>
                        <Link to="/register">Register</Link>
                    </>
                )}
            </nav>
        </header>
    );
}

export default Header;
