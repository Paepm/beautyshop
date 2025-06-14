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

            // Fehler zurücksetzen
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
        return (
            <div className="flex flex-col items-center justify-center text-center py-20 px-4 bg-gray-100 rounded">
                <img
                    src="/media/shop_page/cart_img.png"
                    alt="Empty Cart"
                    className="w-20 h-20 mb-4"
                />
                <h2 className="text-2xl font-bold mb-2">Your cart is empty.</h2>
                <p className="text-gray-600 mb-6 max-w-md">
                    Browse our wide range of furniture and find your new favorites for every room.
                </p>
                <a
                    href="/productlist"
                    className="inline-block px-6 py-2 bg-black text-white rounded hover:bg-gray-800 transition"
                >
                    Go to Products
                </a>
            </div>
        );
    }

    return (
        <div className="max-w-5xl mx-auto p-4">
            <h2 className="text-2xl font-semibold mb-4">
                {user?.username ? `${user.username}, that is your Cart` : 'Your Cart'}
            </h2>

            <p className="text-sm text-gray-600 mb-6">({cartItems.length} Artikel)</p>

            <div className="space-y-6">
                {cartItems.map((item) => (
                    <div key={item.id} className="flex flex-col md:flex-row justify-between border-b pb-6 gap-6">
                        {/* Produktinformationen */}
                        <div className="flex gap-4 w-full md:w-1/3">
                            <img
                                src={item.product.image}
                                alt={item.product.name}
                                className="w-20 h-20 object-cover rounded shadow"
                            />
                            <div>
                                <Link to={`/products/${item.product.id}`} className="font-medium hover:underline">
                                    {item.product.name}
                                </Link>
                                {quantityErros[item.id] && (
                                    <p className="text-sm text-red-600 font-medium mt-1">{quantityErros[item.id]}</p>
                                )}
                            </div>
                        </div>

                        {/* Quantity-Steuerung & Delete */}
                        <div className="flex items-center gap-2 justify-center md:w-1/3">
                            <button
                                onClick={() => item.quantity > 1 && updateQuantity(item.id, "decrement")}
                                className="px-3 py-1 border rounded"
                            >
                                –
                            </button>
                            <span className="w-8 text-center">{item.quantity}</span>
                            <button
                                onClick={() => updateQuantity(item.id, "increment")}
                                className="px-3 py-1 border rounded"
                            >
                                +
                            </button>
                            <button
                                onClick={() => removeFromCart(item.id)}
                                className="ml-4 px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700 transition"
                            >
                                ✖
                            </button>
                        </div>

                        {/* Rechte Tabelle */}
                        <div className="text-sm text-right md:w-1/3">
                            <div>Price per Unit: <span className="font-medium">€{item.product.price.toFixed(2)}</span></div>
                            <div>Quantity: <span className="font-medium">{item.quantity}</span></div>
                            <div className="mt-1">Subtotal: <span className="font-semibold text-lg">€{(item.quantity * item.product.price).toFixed(2)}</span></div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Summary & Checkout */}
            <div className="mt-10 text-right">
                <p className="font-semibold text-xl mb-2">Summary: €{totalPrice.toFixed(2)}</p>
                <a
                    href="/checkout/"
                    className="inline-block px-6 py-2 bg-black text-white rounded hover:bg-gray-800 transition"
                >
                    Proceed to Checkout
                </a>
            </div>
        </div>
    );

}

export default CartPage;
