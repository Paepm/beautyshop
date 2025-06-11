import { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { useCart } from "../contexts/CartContext";
import { AuthContext } from '../contexts/AuthContext';

const CartPage = () => {
    const [cartItems, setCartItems] = useState([]);
    const [totalPrice, setTotalPrice] = useState(0);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const { refreshCart } = useCart();
    const { user } = useContext(AuthContext);
    const [quantityErros, setQuantityErrors] = useState({});


    useEffect(() => {
        fetchCart();
    }, []);

    const fetchCart = async () => {
        try {
            const response = await api.get("cart/");
            setCartItems(response.data.items);
            setTotalPrice(response.data.total_price ?? 0);
        } catch (error) {
            console.error("Issue fetching cart:", error);
            setError("Issue fetching cart. Please try again later.");
        } finally {
            setIsLoading(false);
        }
    };

    const updateQuantity = async (itemId, action = null, quantity = null) => {
        try {
            const formData = new FormData();
            if (action) formData.append('action', action);
            if (quantity !== null) formData.append('quantity', parseInt(quantity));

            await api.post(`cart/update/${itemId}/`, formData);
            refreshCart();
            fetchCart();

            // ✅ Fehler zurücksetzen
            setQuantityErrors(prev => ({ ...prev, [itemId]: null }));
        } catch (error) {
            console.error('Error by changing quantity:', error);

            if (error.response?.status === 400 && error.response?.data?.detail) {
                setQuantityErrors(prev => ({ ...prev, [itemId]: error.response.data.detail }));
            } else {
                setQuantityErrors(prev => ({ ...prev, [itemId]: 'Out of Stock' }));
            }
        }
    };



    const removeFromCart = async (ItemId) => {
        try {
            await api.delete(`cart/remove/${ItemId}/`);
            refreshCart(); // refresh cart count in context
            fetchCart(); // reload cart after removal
        } catch (error) {
            console.error('Error by delete product:', error);
        }
    };


    if (isLoading) return <p className="p-4"> Cart is loading....</p>;
    if (error) return <p className="p-4 text-red-500">{error}</p>;
    if (cartItems.length === 0) {
        return <p className="p-4">Your cart is empty.</p>;
    }

    return (
        <div className="max-w-4xl mx-auto p-4">
            <h2 className="text-2xl font-semibold mb-4">
                {user?.username ? `${user.username}, that is your Cart` : 'Your Cart'}
            </h2>

            <p className="text-sm text-gray-600 mb-6">({cartItems.length} Artikle)</p>

            <ul className="space-y-6">
                {cartItems.map((item) => (
                    <li key={item.id} className="flex justify-between items-center border-b pb-4">
                        <div>
                            <Link to={`/products/${item.product.id}`} className="flex items-center gap-4">
                                <img
                                    src={item.product.image}
                                    alt={item.product.name}
                                    className="w-16 h-16 object-cover rounded shadow"
                                />
                                <p className="font-medium">{item.product.name}</p>
                            </Link>
                            <p className="text-sm text-gray-600">
                                {item.quantity} × €{item.product.price.toFixed(2)}
                            </p>
                            <p className="text-sm text-gray-800">
                                Subtotal: €{(item.quantity * item.product.price).toFixed(2)}
                            </p>
                            {quantityErros[item.id] && (
                                <p className="text-sm text-red-600 font-medium">{quantityErros[item.id]}</p>
                            )}
                        </div>


                        <div className="flex items-center gap-2">
                            <button
                                onClick={() => {
                                    if (item.quantity > 1) {
                                        updateQuantity(item.id, "decrement");
                                    }
                                }}
                                className="px-2 py-1 border rounded"
                            >
                                –
                            </button>

                            <span className="w-6 text-center">{item.quantity}</span>

                            <button
                                onClick={() => updateQuantity(item.id, "increment")}
                                className="px-2 py-1 border rounded"
                            >
                                +
                            </button>
                            <button
                                onClick={() => removeFromCart(item.id)}
                                className="ml-4 px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700 transition"
                            >
                                delete
                            </button>
                        </div>
                    </li>

                ))}
            </ul>

            <div className="mt-8 text-right font-semibold text-lg">
                Summary: €{totalPrice.toFixed(2)}
            </div>
            <a href="/checkout/" className="px-4 py-2 bg-black text-white rounded hover:bg-gray-800">
                Proceed to Checkout
            </a>

        </div>
    );
}

export default CartPage;
