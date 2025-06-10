import { useNavigate, useParams, Link } from 'react-router-dom';
import { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../contexts/AuthContext';
import api from '../services/api';

function ProductDetailPage() {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { isAuthenticated } = useContext(AuthContext);
    const navigate = useNavigate();
    const [added, setAdded] = useState(false);
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
            setAdded(true);
            setTimeout(() => setAdded(false), 2000);
        } catch (error) {
            setError('Out of stock');
            setTimeout(() => setError(''), 1000);
        }
    };

    if (loading) return <p className="p-6 text-center text-gray-500">Loading product details...</p>;
    if (error) return <p className="p-6 text-center text-red-600">{error}</p>;
    if (!product) return null;


    return (
        <div className="max-w-5xl mx-auto p-6 grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
            <div className="w-full">
                <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-auto object-cover rounded-xl shadow-md"
                />
            </div>

            <div className="space-y-6">
                <h1 className="text-4xl font-bold text-gray-900">{product.name}</h1>

                <p className="text-gray-600 text-lg">{product.description}</p>

                <p className="text-2xl font-semibold text-gray-800">
                    {product.price_current} €
                </p>

                {product.stock === 0 && (
                    <p className="text-red-600 font-medium text-md">Out of stock</p>
                )}

                <div className="flex flex-col sm:flex-row gap-4">
                    <button
                        onClick={handleAddToCart}
                        disabled={product.stock === 0}
                        className={`px-6 py-3 text-white font-semibold rounded transition-colors ${product.stock === 0
                            ? "bg-gray-400 cursor-not-allowed"
                            : "bg-black hover:bg-gray-800"
                            }`}
                    >
                        {product.stock === 0 ? "Not Available" : "Add to Cart"}
                    </button>

                    <Link to="/">
                        <button className="px-6 py-3 border border-gray-400 text-gray-800 rounded hover:bg-gray-100">
                            Back to Products
                        </button>
                    </Link>
                </div>
            </div>
        </div>
    );
}

export default ProductDetailPage;

