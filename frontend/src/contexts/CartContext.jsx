// contexts/CartContext.js

import { createContext, useContext, useState, useEffect } from "react";
import api from "../services/api";

export const CartContext = createContext();

export function CartProvider({ children }) {
    const [cartCount, setCartCount] = useState(0);

    const fetchCart = async () => {
        try {
            const res = await api.get("/cart/");
            const items = res.data.items || [];
            const count = items.reduce((sum, item) => sum + item.quantity, 0);
            setCartCount(count);
        } catch (err) {
            console.error("Cart fetch failed", err);
        }
    };

    useEffect(() => {
        fetchCart();
    }, []);

    return (
        <CartContext.Provider value={{ cartCount, refreshCart: fetchCart }}>
            {children}
        </CartContext.Provider>
    );
}

export const useCart = () => useContext(CartContext);
