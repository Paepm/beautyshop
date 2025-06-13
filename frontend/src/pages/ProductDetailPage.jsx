import { useNavigate, useParams, Link } from 'react-router-dom';
import { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import api from '../services/api';
import { useCart } from '../contexts/CartContext';

function ProductDetailPage() {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { isAuthenticated } = useContext(AuthContext);
    const navigate = useNavigate();
    const [added, setAdded] = useState(false);
    const [quantity, setQuantity] = useState(1);
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const { refreshCart } = useCart();
    const [outOfStockNotice, setOutOfStockNotice] = useState(false);




    useEffect(() => {
        api.get(`/products/${id}/`)
            .then(res => {
                setProduct(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Error loading product:", err);
                setError("Unable to load product.");
                setLoading(false);
            });
    }, [id]);

    const handlePrevImage = () => {
        console.log("← clicked");
        if (!product.images || product.images.length <= 1) return;
        console.log("Aktuelles Bild:", product.images?.[currentImageIndex]);

        setCurrentImageIndex((prev) => (prev === 0 ? product.images.length - 1 : prev - 1));
    };

    const handleNextImage = () => {
        console.log("→ clicked");
        if (!product.images || product.images.length <= 1) return;
        console.log("Aktuelles Bild:", product.images?.[currentImageIndex]);

        setCurrentImageIndex((prev) => (prev === product.images.length - 1 ? 0 : prev + 1));
    };


    const handleAddToCart = async () => {
        setError('');
        if (!isAuthenticated) {
            navigate('/login');
            return;
        }

        if (product.stock === 0 || !product.available) {
            setOutOfStockNotice(true);
            setTimeout(() => setOutOfStockNotice(false), 3000);
            return;
        }

        try {
            const formData = new URLSearchParams();
            formData.append('action', 'increment');
            formData.append('quantity', quantity);
            await api.post(`cart/add/${product.id}/`, formData);
            refreshCart();
            setAdded(true);
            setTimeout(() => setAdded(false), 2000);
        } catch (error) {
            setOutOfStockNotice(true);
            setTimeout(() => setOutOfStockNotice(false), 3000);
        }
    };


    if (loading) return <p className="p-6 text-center text-gray-500">Loading product details...</p>;
    if (error) return <p className="p-6 text-center text-red-600">{error}</p>;
    if (!product) return null;

    // Lieferzeit (2–5 Werktage)
    const today = new Date();
    const deliveryStart = new Date(today);
    deliveryStart.setDate(today.getDate() + 2);
    const deliveryEnd = new Date(today);
    deliveryEnd.setDate(today.getDate() + 5);
    const deliveryText = `ca. ${deliveryStart.toLocaleDateString()} – ${deliveryEnd.toLocaleDateString()} available`;

    return (

        <div className="max-w-5xl mx-auto p-6 grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
            <div className="w-full relative">
                {product.images && product.images.length > 0 && (
                    <div className="relative">
                        {product.sale && product.discount_percent && (
                            <div className="absolute top-2 left-2 bg-red-600 text-white text-xs font-bold px-2 py-1 rounded shadow z-30">
                                -{product.discount_percent}%
                            </div>
                        )}
                        <img
                            src={product.images?.[currentImageIndex]?.image || product.image}
                            alt={product.name}
                            className="w-full h-auto object-contain rounded-xl shadow-md max-h-[450px]"
                            key={product.images?.[currentImageIndex]?.image || product.image}
                        />
                        {product.images.length > 1 && (
                            <>
                                <button
                                    type="button"
                                    onClick={handlePrevImage}
                                    className="absolute left-0 top-1/2 transform -translate-y-1/2 bg-white px-2 py-1 shadow rounded-l z-20 pointer-events-auto"
                                >
                                    ◀
                                </button>
                                <button
                                    type="button"
                                    onClick={handleNextImage}
                                    className="absolute right-0 top-1/2 transform -translate-y-1/2 bg-white px-2 py-1 shadow rounded-r z-20 pointer-events-auto"
                                >
                                    ▶
                                </button>
                            </>
                        )}
                    </div>
                )}
            </div>

            <div className="space-y-6">
                <h1 className="text-4xl font-bold text-gray-900">{product.name}</h1>

                {product.sale ? (
                    <div>
                        <p className="text-2xl font-bold text-red-600">{product.price_current} €</p>
                        <p className="line-through text-gray-500 text-sm">{product.price_old} €</p>
                    </div>
                ) : (
                    <p className="text-2xl font-semibold text-gray-800">{product.price_current} €</p>
                )}


                <p className="text-green-600 text-sm">{deliveryText}</p>

                <div className="relative">
                    <label className="block text-sm mb-1">Quantity:</label>
                    <select
                        value={quantity}
                        onChange={(e) => setQuantity(parseInt(e.target.value))}
                        className="border px-3 py-2 rounded w-24"
                    >
                        {[...Array(10)].map((_, i) => (
                            <option key={i + 1} value={i + 1}>{i + 1}</option>
                        ))}
                    </select>
                    {outOfStockNotice && (
                        <span className="absolute left-28 top-0 text-sm text-red-600 font-medium">
                            Out of stock
                        </span>
                    )}
                </div>

                <div className="flex flex-col sm:flex-row gap-4">
                    <button
                        onClick={handleAddToCart}
                        disabled={product.stock === 0}
                        className={`px-6 py-3 text-white font-semibold rounded transition-colors ${product.stock === 0
                            ? "bg-gray-400 cursor-not-allowed"
                            : "bg-black hover:bg-gray-800"
                            }`}
                    >
                        {added ? "Added" : product.stock === 0 ? "Not available" : "Add to Cart"}
                    </button>

                    <Link to="/productlist">
                        <button className="px-6 py-3 border border-gray-400 text-gray-800 rounded hover:bg-gray-100">
                            Back to Products
                        </button>
                    </Link>
                </div>

                <div className="pt-6 border-t">
                    <h2 className="text-lg font-semibold mb-2">Description</h2>
                    <p className="text-gray-700 whitespace-pre-wrap">{product.description}</p>
                </div>
            </div>
        </div>
    );
}

export default ProductDetailPage;
