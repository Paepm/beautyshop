import { Link, useNavigate } from 'react-router-dom';
import { useContext, useState } from 'react';
import LogoutButton from '../LogoutButton';
import { AuthContext } from '../../contexts/AuthContext';
import { useCart } from '../../contexts/CartContext';

function Header() {
    const { isAuthenticated } = useContext(AuthContext);
    const { cartCount } = useCart();
    const [searchTerm, setSearchTerm] = useState("");
    const navigate = useNavigate();

    const handleSearchSubmit = (e) => {
        e.preventDefault();
        const params = new URLSearchParams();
        if (searchTerm) params.set("search", searchTerm);
        navigate({ pathname: "/productlist", search: params.toString() });
    };

    return (
        <header className="p-4 shadow bg-white flex flex-wrap items-center justify-between gap-4">
            <Link to="/" className="flex items-center space-x-4">
                <div className="relative w-60 h-0">
                    <img
                        src="http://localhost:8000/media/shop_page/WohnsSinn_logo1.png"
                        alt="Logo"
                        className="absolute top-[-30px] left-0 h-16 drop-shadow-md hover:scale-105 transition-transform"
                    />
                </div>
            </Link>

            {/* search field with button */}
            <form onSubmit={handleSearchSubmit} className="flex flex-1 max-w-md border rounded shadow-sm overflow-hidden">
                <input
                    type="text"
                    placeholder="Search products..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="flex-grow px-4 py-2 outline-none"
                />
                <button
                    type="submit"
                    className="bg-yellow-300 px-4 text-black hover:bg-yellow-400 transition-all"
                >
                    🔍
                </button>
            </form>

            <nav className="flex justify-end items-center space-x-4 col-start-3">
                {isAuthenticated ? (
                    <>
                        <nav className="flex gap-6 items-center">
                            <Link to="/cart" className="relative">
                                <span className="text-2xl">🛒</span>
                                {cartCount > 0 && (
                                    <span className="absolute -top-2 -right-2 bg-red-600 text-white text-xs font-bold rounded-full px-2 py-0.5">
                                        {cartCount}
                                    </span>
                                )}
                            </Link>
                        </nav>
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
