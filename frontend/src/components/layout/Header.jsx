import { Link } from 'react-router-dom';
import { useContext } from 'react';

import { AuthContext } from '../../contexts/AuthContext';
import LogoutButton from '../LogoutButton';

function Header() {
    const { isAuthenticated, user } = useContext(AuthContext);


    return (
        <header className="p-4 shadow bg-white flex justify-between items-center">
            <Link to="/" className="flex items-center space-x-4">
                <div className="relative w-60 h0">
                    <img
                        src="http://localhost:8000/media/shop_page/WohnsSinn_logo1.png"
                        alt="Logo"
                        className="absolute top-[-30px] left-0 h-16 drop-shadow-md hover:scale-105 transition-transform"
                    />
                </div>
            </Link>
            {isAuthenticated && user && (
                <h1 className="text-center text-gray-700 text-lg font-medium col-start-2">
                    Hello {user.username}, have fun with shopping!
                </h1>
            )}
            <nav className="flex justify-end items-center space-x-4 col-start-3">
                {isAuthenticated ? (
                    <>
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
                        <Link to="/profile">Profile</Link>
                        <LogoutButton />
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
