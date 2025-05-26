import React from 'react';
import api from '../services/api';

function ProductCard({ product }) {
    const handleAddToCart = async () => {
        try {
            await api.post(`/cart/add/${product.id}/`);
            alert('Produkt wurde zum Warenkorb hinzugefügt!');
        } catch (error) {
            console.error('Fehler beim Hinzufügen zum Warenkorb:', error);
            alert('Fehler beim Hinzufügen zum Warenkorb');
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
                In den Warenkorb
            </button>
        </div>
    );
}

export default ProductCard;
