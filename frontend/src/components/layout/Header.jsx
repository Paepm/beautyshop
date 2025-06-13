import { Link, useNavigate } from 'react-router-dom';
import { useContext, useEffect, useRef, useState } from 'react';
import LogoutButton from '../LogoutButton';
import { AuthContext } from '../../contexts/AuthContext';
import { useCart } from '../../contexts/CartContext';

function Header() {
    const { isAuthenticated } = useContext(AuthContext);
    const { cartCount } = useCart();
    const [searchTerm, setSearchTerm] = useState("");
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const dropdownRef = useRef();
    const navigate = useNavigate();

    const handleSearchSubmit = (e) => {
        e.preventDefault();
        const params = new URLSearchParams();
        if (searchTerm) params.set("search", searchTerm);
        navigate({ pathname: "/productlist", search: params.toString() });
    };

    // Schließt Dropdown bei Klick außerhalb
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setDropdownOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    return (
        <header className="bg-zinc-100 shadow px-6 py-4">
            <div className="max-w-7xl mx-auto flex items-center justify-between gap-4 flex-wrap relative">

                {/* Search */}
                <form
                    onSubmit={handleSearchSubmit}
                    className="absolute left-1/2 transform -translate-x-1/2 w-full max-w-lg flex border border-gray-300 rounded overflow-hidden shadow-sm"
                >
                    <input
                        type="text"
                        placeholder="Search products..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="flex-grow px-4 py-2 outline-none text-sm"
                    />
                    <button
                        type="submit"
                        className="bg-yellow-400 hover:bg-yellow-500 px-4 text-black transition-all shrink-0"
                    >
                        🔍
                    </button>
                </form>

                {/* Navigation */}
                <nav className="flex items-center gap-2 text-sm ml-auto">
                    {isAuthenticated ? (
                        <>
                            <Link
                                to="/cart"
                                className="relative right-10 text-xl hover:scale-110 transition"
                                title="Cart"
                            >
                                🛒
                                {cartCount > 0 && (
                                    <span className="absolute -top-2 -right-2 bg-red-600 text-white text-xs font-bold rounded-full px-2 py-0.5">
                                        {cartCount}
                                    </span>
                                )}
                            </Link>

                            {/* Profile Dropdown */}
                            <div className="relative right-5" ref={dropdownRef}>
                                <button
                                    onClick={() => setDropdownOpen(prev => !prev)}
                                    className="group focus:outline-none"
                                    title="Profile"
                                >
                                    <img
                                        src="/media/shop_page/profile.png"
                                        alt="profile"
                                        className="h-6 transition-transform duration-200 group-hover:-translate-y-0.5 group-hover:scale-110"
                                    />
                                </button>

                                {dropdownOpen && (
                                    <div className="absolute right-0 mt-2 w-40 bg-white border border-gray-300 rounded shadow-lg z-50">
                                        <Link
                                            to="/profile"
                                            className="block px-4 py-2 text-sm hover:bg-gray-100 transition"
                                            onClick={() => setDropdownOpen(false)}
                                        >
                                            Profile Page
                                        </Link>
                                        <Link
                                            to="/orderlist"
                                            className="block px-4 py-2 text-sm hover:bg-gray-100 transition"
                                            onClick={() => setDropdownOpen(false)}
                                        >
                                            My Orders
                                        </Link>
                                        <Link
                                            to="/cart"
                                            className="block px-4 py-2 text-sm hover:bg-gray-100 transition"
                                            onClick={() => setDropdownOpen(false)}>
                                            My Cart
                                        </Link>
                                    </div>
                                )}
                            </div>

                            <LogoutButton />
                        </>
                    ) : (
                        <>
                            <Link
                                to="/login"
                                className="bg-yellow-400 text-black px-3 py-1 rounded hover:bg-yellow-500"
                            >
                                Login
                            </Link>

                            <Link
                                to="/sign_up"
                                className="bg-yellow-400 text-black px-3 py-1 rounded hover:bg-yellow-500"
                            >
                                Register
                            </Link>
                        </>
                    )}
                </nav>
            </div>
        </header>
    );
}

export default Header;
