import api from '../services/api';
import { AuthContext } from '../contexts/AuthContext';
import { useContext, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useCart } from "../contexts/CartContext";

function ProductCard({ product }) {
    const { isAuthenticated } = useContext(AuthContext);
    const navigate = useNavigate();

    const [added, setAdded] = useState(false);
    const [error, setError] = useState('');

    const { refreshCart } = useCart();

    const handleAddToCart = async () => {
        setError('');
        if (!isAuthenticated) {
            navigate('/login');
            return;
        }

        if (product.stock === 0 || !product.available) {
            setError('Product is out of stock ');
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

    return (
        <div className="border rounded-lg shadow-md p-4 flex flex-col items-center hover:shadow-lg transition relative">

            {/* Erfolgs-Badge */}
            {added && (
                <div className="absolute top-2 right-2 bg-green-600 text-white text-xs font-semibold px-2 py-1 rounded shadow">
                    Successfully added
                </div>
            )}

            {/* Fehleranzeige */}
            {error && (
                <div className="absolute top-2 left-2 bg-red-500 text-white text-xs font-semibold px-2 py-1 rounded shadow animate-pulse">
                    {error}
                </div>
            )}

            {/* Klickbarer Bereich für Detailseite */}
            <Link
                to={`/products/${product.id}`}
                className="w-full flex flex-col items-center no-underline text-black"
            >
                <img
                    src={product.image}
                    alt={product.name}
                    className="w-48 h-48 object-cover mb-4"
                />
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
