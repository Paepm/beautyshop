import { createContext, useContext, useEffect, useState } from "react";
import api from "../services/api";

const WishlistContext = createContext();

export const useWishlist = () => useContext(WishlistContext);

export function WishlistProvider({ children }) {
    const [wishlistCount, setWishlistCount] = useState(0);

    const fetchWishlist = async () => {
        try {
            const res = await api.get("wishlist/");
            setWishlistCount(res.data.length);
            return res.data; // <-- Wichtig!
        } catch (error) {
            console.error("Error fetching wishlist", error);
            return []; // <-- Gib leeres Array zurück, damit keine Fehler auftreten
        }
    };


    useEffect(() => {
        fetchWishlist();
    }, []);

    return (
        <WishlistContext.Provider value={{ wishlistCount, fetchWishlist }}>
            {children}
        </WishlistContext.Provider>
    );
}
