import { createContext, useContext, useEffect, useState } from "react";
import api from "../services/api";

const WishlistContext = createContext();

export const useWishlist = () => useContext(WishlistContext);

export function WishlistProvider({ children }) {
    const [wishlistCount, setWishlistCount] = useState(0);
    const [wishlistItems, setWishlistItems] = useState([]);

    const fetchWishlist = async () => {
        try {
            const res = await api.get("wishlist/");
            setWishlistCount(res.data.length);
            setWishlistItems(res.data);
            // console.log("Fetched wishlist:", res.data);
            return res.data; // <-- Wichtig!
        } catch (error) {
            console.error("Error fetching wishlist", error);
            setWishlistItems([]);
            return []; // <-- Gib leeres Array zurück, damit keine Fehler auftreten
        }
    };


    useEffect(() => {
        fetchWishlist();
    }, []);

    return (
        <WishlistContext.Provider value={{ wishlistItems, wishlistCount, fetchWishlist }}>
            {children}
        </WishlistContext.Provider>
    );
}
