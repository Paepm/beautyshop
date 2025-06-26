import { useContext, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useCart } from "../contexts/CartContext";
import { FaHeart } from 'react-icons/fa';

import api, {baseUrl} from '../services/api';
import { AuthContext } from '../contexts/AuthContext';
import { useWishlist } from '../contexts/WishlistContext';

function ProductCard({ product }) {
    const { isAuthenticated } = useContext(AuthContext);
    const navigate = useNavigate();

    const [added, setAdded] = useState(false);
    const [error, setError] = useState('');
    const [wishlistError, setWishlistError] = useState(''); // Zustand für Wishlist-Fehler

    const { refreshCart } = useCart();
    const { wishlistItems, fetchWishlist } = useWishlist();

    const handleAddToCart = async () => {
        console.log("product.image:", product.image);
        setError('');
        if (!isAuthenticated) {
            navigate('/login');
            return;
        }

        if (product.stock === 0 || !product.available) {
            setError('Product is out of stock');
            return;
        }

        try {
            const formData = new URLSearchParams();
            formData.append('action', 'increment');
            formData.append('quantity', 1);
            await api.post(`cart/add/${product.id}/`, formData, {
                responseType: 'json',
            });
            refreshCart();
            setAdded(true);
            setTimeout(() => setAdded(false), 2000);
        } catch (error) {
            setError('Out of stock');
            setTimeout(() => setError(''), 1000);
        }
    };

    const handleWishlistClick = async (e) => {
        e.preventDefault();
        const alreadyInWishlist = wishlistItems?.some(item => item.product.id === product.id);

        if (alreadyInWishlist) {
            setWishlistError('Already in wishlist');
            setTimeout(() => setWishlistError(''), 1000);
            return;
        }

        try {
            await api.post(`/wishlist/add/${product.id}/`);
            await fetchWishlist();
            setWishlistError('Added to wishlist!');
            setTimeout(() => setWishlistError(''), 1000);
        } catch (err) {
            console.error("Error by add Product to wishlist:", err);
            setWishlistError('Error adding to wishlist');
            setTimeout(() => setWishlistError(''), 1000);
        }
    };

    return (
        <div className="border rounded-lg shadow-md p-4 flex flex-col items-center hover:shadow-lg transition relative">

            {/* Erfolgs-Badge */}
            {added && (
                <div className="absolute bottom-2 right-2 bg-green-600 text-white text-xs font-semibold px-2 py-1 rounded shadow">
                    Successfully added
                </div>
            )}

            {/* Fehleranzeige (Cart) */}
            {error && (
                <div className="absolute bottom-2 left-2 bg-red-500 text-white text-xs font-semibold px-2 py-1 rounded shadow animate-pulse">
                    {error}
                </div>
            )}

            {/* Wishlist-Meldung */}
            {wishlistError && (
                <div className={`absolute bottom-2 left-2 text-white text-xs font-semibold px-2 py-1 rounded shadow animate-pulse
                    ${wishlistError === 'Added to wishlist!' ? 'bg-green-600' : 'bg-red-500'}`}>
                    {wishlistError}
                </div>
            )}

            {/* Sale-Badge */}
            {product.sale && product.discount_percent && (
                <div className="absolute top-2 left-2 bg-red-600 text-white text-xs font-bold px-2 py-1 rounded shadow">
                    -{product.discount_percent}%
                </div>
            )}

            {/* Wishlist-Button */}
            {isAuthenticated && (
                <button
                    onClick={handleWishlistClick}
                    className="absolute top-1 right-1 text-white bg-black/50 hover:bg-red-500 p-2 rounded-full"
                    title="Add to Wishlist"
                >
                    <FaHeart className="w-4 h-4" />
                </button>
            )}

            {/* Klickbarer Bereich für Produktdetails */}
            <Link
                to={`/products/${product.id}`}
                className="w-full flex flex-col items-center no-underline text-black"
            >
                <div className="relative w-48 h-48 mb-4">
                    <img
                        src={product.image}
                        alt={product.name}
                        className="w-full h-full object-cover rounded"
                    />
                </div>

                <h2 className="text-lg font-semibold text-center">{product.name}</h2>

                {product.sale ? (
                    <div className="mb-2 text-center">
                        <span className="text-red-600 font-bold text-lg">
                            {product.price_current} €
                        </span>
                        <span className="line-through text-gray-500 text-sm ml-2">
                            {product.price_old} €
                        </span>
                    </div>
                ) : (
                    <p className="text-gray-700 mb-2">{product.price_current} €</p>
                )}

                {!product.available && (
                    <span className="text-sm text-red-600 font-medium">not available</span>
                )}
            </Link>

            {/* Add-to-cart Button */}
            <button
                onClick={handleAddToCart}
                className="mt-auto bg-black text-white px-4 py-2 rounded hover:bg-gray-800 transition-colors disabled:opacity-50"
                disabled={product.stock === 0 || !product.available}
            >
                Add to cart
            </button>
        </div>
    );
}

export default ProductCard;
