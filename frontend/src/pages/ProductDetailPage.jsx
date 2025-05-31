import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import api from '../services/api';

function ProductDetailPage() {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

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

    if (loading) return <p className="p-6 text-center text-gray-500">Loading product details...</p>;
    if (error) return <p className="p-6 text-center text-red-600">{error}</p>;
    if (!product) return null;

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-4">{product.name}</h1>
            <img
                src={product.image}
                alt={product.name}
                className="w-64 h-64 object-cover rounded mb-6 shadow"
            />
            <p className="text-gray-700 text-lg mb-4">{product.description}</p>
            <p className="text-xl font-semibold mb-6">{product.price} €</p>

            <button
                className="bg-black text-white px-6 py-3 rounded hover:bg-gray-800 transition-colors"
                onClick={() => alert('Add to cart functionality coming soon!')}
            >
                Add to Cart
            </button>

            <button className="bg-black text-white px-6 py-3 rounded hover:bg-gray-800 transition-colors">
                Back To Products</button>
        </div>
    );
}

export default ProductDetailPage;
