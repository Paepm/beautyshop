/**
 * CartPage
 *
 * This component displays the user's current cart, including:
 * - A list of products in the cart
 * - Quantity controls (+ / - / input field)
 * - Remove product button
 * - Total cart price
 */

import React, { useEffect, useState } from 'react';
import api from '../services/api';


const CartPage = () => {
    const [cartItems, setCartItems] = useState([]);
    const [totalPrice, setTotalPrice] = useState(0);
    const [isLoading, setIsLoading] = useState(true);

    /**
     * Fetch cart data from the backend when the component mounts.
     */
    useEffect(() => {
        fetchCart();
    }, []);

    /**
     * Fetch the cart items and total price from the API.
     */
    const fetchCart = async () => {
        try {
            const respone = await api.get('cart/');
            setCartItems(respone.data.cart_items);
            setTotalPrice(respone.data.total_price);
        } catch (error) {
            console.error('Error fetching cart data:', error);
        } finally {
            setIsLoading(false);
        }
    };

    /**
     * Handle quantity update for a specific cart item.
     * 
     * @param {number} itemId - The ID of the cart item to update.
     * @param {"increment" | "decrement" | "null"} action - The action to perform on the quantity.
     * @param {number|null} quantity - The new quantity (if set manually).
     */

    const updateQuantity = async (itemId, action = null, quantity = null) => {
        try {
            const formData = new FormData();
            if (action) formData.append('action', action);
            if (quantity) formData.append('quantity', quantity);
            await api.post(`cart/"/update/${itemId}`, formData);
            fetchCart(); // Refresh the cart after updating
        } catch (error) {
            console.error('Error updating cart item quantity:', error);
        }
    };

    /**
     * Remove a product from the cart.
     *
     * @param {number} productId - The ID of the product to remove.
     */
    const removeFromCart = async (productId) => {
        try {
            await api.post(`/cart/remove/${productId}/`);
            fetchCart(); // Refresh the cart after removing

        } catch (error) {
            console.error('Error removing product from cart:', error);
        }
    };
    if (isLoading) return <p className="p-4">Loading cart...</p>;

    if (cartItems.length === 0) {
        return <p className="p-4">Your cart is empty</p>;
    }

    return (<div className="max-w-4xl mx-auto p-4">
        <h2 className="text-2xl font-semibold mb-4">Your Cart</h2>
        <ul className="space-y-4">
            {cartItems.map((item) => (
                <li key={item.id} className="flex justify-between items-center border-b pb-4">
                    <div>
                        <p className="font-medium">{item.product.name}</p>
                        <p className="text-sm text-gray-600">
                            {item.quantity} × €{item.product.price.toFixed(2)}
                        </p>
                        <p className="text-sm text-gray-800">
                            Subtotal: €{(item.quantity * item.product.price).toFixed(2)}
                        </p>
                    </div>

                    <div className="flex items-center gap-2">
                        <button
                            onClick={() => updateQuantity(item.id, "decrement")}
                            className="px-2 py-1 border rounded"
                        >
                            −
                        </button>
                        <input
                            type="number"
                            min="1"
                            value={item.quantity}
                            onChange={(e) => updateQuantity(item.id, null, e.target.value)}
                            className="w-14 border rounded text-center"
                        />
                        <button
                            onClick={() => updateQuantity(item.id, "increment")}
                            className="px-2 py-1 border rounded"
                        >
                            +
                        </button>
                        <button
                            onClick={() => removeFromCart(item.product.id)}
                            className="ml-4 px-3 py-1 text-red-600 hover:underline"
                        >
                            Remove
                        </button>
                    </div>
                </li>
            ))}
        </ul>

        <div className="mt-6 text-right font-semibold text-lg">
            Total: €{totalPrice.toFixed(2)}
        </div>
    </div>
    );
};

export default CartPage;
