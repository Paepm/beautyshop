import { Link, useNavigate } from 'react-router-dom';
import { useContext, useEffect, useRef, useState } from 'react';
import { ShoppingCart, HeartHandshake, UserRound } from "lucide-react";

import LogoutButton from '../LogoutButton';
import { AuthContext } from '../../contexts/AuthContext';
import { useCart } from '../../contexts/CartContext';
import { useWishlist } from '../../contexts/WishlistContext';



function Header() {
    const { isAuthenticated, user } = useContext(AuthContext);
    const { cartCount } = useCart();
    const { wishlistCount } = useWishlist();
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
        <header className="bg-zinc-100 shadow py-4 relative">
            <div className="max-w-5xl mx-auto relative">
                {/* Suchleiste – zentriert */}
                <form
                    onSubmit={handleSearchSubmit}
                    className="mx-auto max-w-xl flex border border-gray-300 rounded overflow-hidden shadow-sm"
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

                {/* Icons */}
                <div className="absolute top-1/2 -translate-y-1/2 left-[calc(50%+350px)] flex items-center gap-6">
                    {isAuthenticated ? (
                        <>
                            {/* Profile */}
                            <div className="group flex flex-col items-center relative" ref={dropdownRef}>
                                <button
                                    onClick={() => setDropdownOpen(prev => !prev)}
                                    className="focus:outline-none flex flex-col items-center"
                                    title="Profile"
                                >
                                    <UserRound className="w-6 h-6 text-gray-800 group-hover:text-blue-500 transition" />
                                    <span className="text-xs mt-1 text-gray-800 group-hover:text-blue-500 transition">Profile</span>
                                </button>

                                {/* Dropdown-Menü */}
                                {dropdownOpen && (
                                    <div className="absolute top-10 w-40 bg-white border border-gray-300 rounded shadow-lg z-50">
                                        <p className="block px-4 py-2 text-sm font-medium text-gray-800 border-b border-gray-200">
                                            Hello {user.username}
                                        </p>
                                        <Link to="/profile" className="block px-4 py-2 text-sm hover:bg-gray-100 transition">My Profile</Link>
                                        <Link to="/orderlist" className="block px-4 py-2 text-sm hover:bg-gray-100 transition">My Orders</Link>
                                        <Link to="/wishlist" className="block px-4 py-2 text-sm hover:bg-gray-100 transition">My Wishlist</Link>
                                        <Link to="/cart" className="block px-4 py-2 text-sm hover:bg-gray-100 transition">My Cart</Link>
                                        <hr className="border-t border-gray-200 my-1" />
                                        <LogoutButton />
                                    </div>
                                )}
                            </div>

                            {/* Wishlist */}
                            <Link to="/wishlist" className="group flex flex-col items-center relative" title="Wishlist">
                                <HeartHandshake className="w-6 h-6 text-gray-800 group-hover:text-red-500 transition" />
                                {wishlistCount > 0 && (
                                    <span className="absolute -top-1 -right-2 bg-red-500 text-white text-xs font-bold rounded-full px-1.5">
                                        {wishlistCount}
                                    </span>
                                )}
                                <span className="text-xs mt-1 text-gray-800 group-hover:text-red-500 transition">Wishlist</span>
                            </Link>


                            {/* Cart */}
                            <Link to="/cart" className="group flex flex-col items-center relative" title="Cart">
                                <ShoppingCart className="w-6 h-6 text-gray-800 group-hover:text-green-500 transition" />
                                {cartCount > 0 && (
                                    <span className="absolute -top-1 -right-2 bg-green-500 text-white text-xs font-bold rounded-full px-1.5">
                                        {cartCount}
                                    </span>
                                )}
                                <span className="text-xs mt-1 text-gray-800 group-hover:text-green-500 transition">Cart</span>
                            </Link>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="bg-yellow-400 text-black px-3 py-1 rounded hover:bg-yellow-500">
                                Login
                            </Link>
                            <Link to="/sign_up" className="bg-yellow-400 text-black px-3 py-1 rounded hover:bg-yellow-500">
                                Register
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </header>
    );
}

export default Header;
