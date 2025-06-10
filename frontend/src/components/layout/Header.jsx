import { Link } from 'react-router-dom';
import { useContext } from 'react';

import { AuthContext } from '../../contexts/AuthContext';
import LogoutButton from '../LogoutButton';

function Header() {
    const { isAuthenticated, user } = useContext(AuthContext);


    return (
        <header className="p-4 shadow bg-white flex justify-between items-center">
            <Link to="/" className="text-2xl font-bold text-gray-800">
                BeautyShop
            </Link>
            {isAuthenticated && user && (
                <h1 className="text-lg font-medium text-center text-gray-700">
                    Hello {user.username}, have fun with shopping!
                </h1>
            )}
            <nav className="space-x-4">
                {isAuthenticated ? (
                    <>
                        <LogoutButton />
                        <Link to="/profile">Profile</Link>
                        <Link
                            to="/cart"
                            className="flex items-center gap-1 text-sm px-3 py-1 border rounded hover:bg-gray-100"
                        >
                            🛒 <span>Go to Cart</span>
                        </Link>
                        <Link
                            to="/orderlist"
                            className="flex items-center gap-1 text-sm px-3 py-1 border rounded hover:bg-gray-100"
                        >
                            📝 <span>My Orders</span>
                        </Link>
                    </>
                ) : (
                    <>
                        <Link to="/login">Login</Link>
                        <Link to="/sign_up">Register</Link>

                    </>
                )}
            </nav>
        </header>
    );
}

export default Header;
