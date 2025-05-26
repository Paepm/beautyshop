import React, { useEffect, useState } from 'react';
import api from '../services/api';
import ProductCard from './ProductCard';


function ProductList() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await api.get('products/');
                setProducts(response.data);
            } catch (error) {
                console.error('Error fetching products:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }
        , []);

    if (loading) return <p>Loading products</p>;

    return (
        <div className="product-list">
            {products.length === 0 ? (
                <p>No products available</p>
            ) : (
                products.map(product => (
                    <ProductCard key={product.id} product={product} />
                ))
            )}
        </div>
    );
}
export default ProductList;