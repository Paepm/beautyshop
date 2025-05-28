import React from 'react';
import api from '../services/api';

function ProductCard({ product }) {
    const handleAddToCart = async () => {
        try {
            await api.post(`/cart/add/${product.id}/`);
            alert('Product added to cart successfully!');
        } catch (error) {
            console.error('Error add to cart:', error);
            alert('Issue adding product to cart. Please try again later.');
        }
    };

    return (
        <div className="border rounded-lg shadow-md p-4 flex flex-col items-center">
            <img
                src={product.image}
                alt={product.name}
                className="w-48 h-48 object-cover mb-4"
            />
            <h2 className="text-lg font-semibold">{product.name}</h2>
            <p className="text-gray-700 mb-2">{product.price} €</p>
            <button
                onClick={handleAddToCart}
                className="mt-auto bg-black text-white px-4 py-2 rounded hover:bg-gray-800"
            >
                Add to Cart
            </button>
        </div>
    );
}

export default ProductCard;
