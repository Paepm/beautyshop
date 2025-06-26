import { useEffect, useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";

import api, {baseUrl} from "../services/api";
import { AuthContext } from "../contexts/AuthContext";
import { useCart } from "../contexts/CartContext";
import { useWishlist } from "../contexts/WishlistContext";

const WishlistPage = () => {
    const [wishlistItems, setWishlistItems] = useState([]);
    const [quantities, setQuantities] = useState({});
    const { isAuthenticated, loading, user } = useContext(AuthContext);
    const { refreshCart } = useCart();
    const { fetchWishlist } = useWishlist();
    const navigate = useNavigate();
    const [cartMessage, setCartMessage] = useState({});

    useEffect(() => {
        if (loading || !isAuthenticated) return;

        const loadWishlist = async () => {
            const data = await fetchWishlist();
            setWishlistItems(data);

            const defaultQuantities = {};
            data.forEach(item => {
                defaultQuantities[item.product.id] = 1;
            });
            setQuantities(defaultQuantities);
        };

        loadWishlist();
    }, [isAuthenticated, loading]);

    const handleRemove = async (productId) => {
        try {
            await api.delete(`wishlist/remove/${productId}/`);
            const updated = await fetchWishlist();
            setWishlistItems(updated);
        } catch (error) {
            console.error("Failed to remove product", error);
        }
    };

    const handleAddToCart = async (productId, quantity) => {
        try {
            const formData = new URLSearchParams();
            formData.append('action', 'increment');
            formData.append('quantity', quantity);

            await api.post(`cart/add/${productId}/`, formData);
            refreshCart();

            // success message
            setCartMessage(prev => ({
                ...prev,
                [productId]: "added to cart!",
            }));
        } catch (error) {
            const msg =
                error?.response?.data?.error ||
                'Error adding to cart. Try again later.';

            console.log("ASDADSD", msg);
            setCartMessage(prev => ({
                ...prev,
                [productId]: msg,
            }));

            setTimeout(() => {
                setCartMessage(prev => ({ ...prev, [productId]: '' }));
            }, 1000);
        }
    }

    if (wishlistItems.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center text-center py-20 px-4 bg-gray-100 rounded">
                <img
                    src="/media/shop_page/empty_wishlist.png"
                    alt="Empty Wishlist"
                    className="w-25 h-20 mb-4"
                />
                <h2 className="text-2xl font-bold mb-2">{user.username}, your wishlist is empty.</h2>
                <p className="text-gray-600 mb-6 max-w-md">
                    Add a Product to your wishlist.
                </p>
                <button
                    className="inline-block px-6 py-2 bg-black text-white rounded hover:bg-gray-800 transition"
                    onClick={() => navigate("/productlist")}
                >
                    Go to Products
                </button>
            </div>
        );
    }

    return (
        <div className="max-w-5xl mx-auto p-4">
            <h2 className="text-2xl font-semibold mb-4">
                {user?.username ? `${user.username}, this is your wishlist` : 'Your Wishlist'}
            </h2>
            <div className="space-y-6">
                {wishlistItems.map((item) => (
                    <div
                        key={item.id}
                        className="flex flex-col md:flex-row justify-between border-b pb-6 gap-6"
                    >
                        {/* Produktinfos */}
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
                            </div>
                        </div>

                        {/* Dropdown + Buttons */}
                        <div className="flex flex-col md:flex-row items-center justify-end md:w-2/3 gap-2 md:gap-4">
                            <select
                                value={quantities[item.product.id]}
                                onChange={(e) =>
                                    setQuantities({
                                        ...quantities,
                                        [item.product.id]: parseInt(e.target.value),
                                    })
                                }
                                className="border border-gray-300 rounded px-2 py-1"
                            >
                                {Array.from({ length: 10 }, (_, i) => i + 1).map((num) => (
                                    <option key={num} value={num}>
                                        {num}
                                    </option>
                                ))}
                            </select>
                            <button
                                onClick={() => handleRemove(item.product.id)}
                                className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
                            >
                                ✖
                            </button>
                            <div className="flex flex-col items-center min-w-[120px]">
                                <button
                                    onClick={() => handleAddToCart(item.product.id, quantities[item.product.id])}
                                    className="px-4 py-2 bg-black text-white rounded hover:bg-gray-800 transition"
                                >
                                    Add to cart
                                </button>

                                {cartMessage[item.product.id] && (
                                    <div className={`text-sm mt-3 text-right ${cartMessage[item.product.id].startsWith('added') ? 'text-green-600' : 'text-red-600'
                                        }`}>
                                        {cartMessage[item.product.id]}
                                    </div>
                                )}
                            </div>


                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default WishlistPage;
