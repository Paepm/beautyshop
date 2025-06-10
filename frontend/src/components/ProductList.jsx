import React, { useEffect, useState } from 'react';
import api from '../services/api';
import ProductCard from './ProductCard';

function ProductList() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [category, setCategory] = useState('');
    const [filterSale, setFilterSale] = useState(false);
    const [filterIsAvailable, setFilterIsAvailable] = useState(false);

    const categories = [
        'chairs',
        'benches',
        'cloth hanger',
        'tables',
        'shelves',
        'trash Cans',
        'trolleys',
        'other',
    ];

    useEffect(() => {
        const fetchProducts = async () => {
            setLoading(true);
            try {
                const params = new URLSearchParams();
                if (category) params.append('category', category);
                if (filterSale) params.append('sale', 'true');
                if (filterIsAvailable) params.append('available', 'true');

                const url = params.toString()
                    ? `products/?${params.toString()}`
                    : 'products/';

                const response = await api.get(url);
                setProducts(response.data);
            } catch (error) {
                console.error('Error fetching products:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, [category, filterSale, filterIsAvailable]); // refresh on category OR sale filter change

    return (
        <div className="product-list-wrapper">
            <div className="mb-4 flex items-center gap-4 flex-wrap">
                <label htmlFor="category" className="font-semibold">Filter by category:</label>
                <select
                    id="category"
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="border px-3 py-1 rounded"
                >
                    <option value="">All</option>
                    {categories.map((cat) => (
                        <option key={cat} value={cat}>
                            {cat.charAt(0).toUpperCase() + cat.slice(1).replace('_', ' ')}
                        </option>
                    ))}
                </select>

                <label className="flex items-center gap-2">
                    <input
                        type="checkbox"
                        checked={filterSale}
                        onChange={(e) => setFilterSale(e.target.checked)}
                        className="form-checkbox"
                    />
                    show offers only
                </label>
                <label className="flex items-center gap-2">
                    <input type="checkbox"
                        checked={filterIsAvailable}
                        onChange={(e) => setFilterIsAvailable(e.target.checked)}
                        className="form-checkbox"
                    />
                    is available
                </label>
            </div>

            {loading ? (
                <p>Loading products…</p>
            ) : products.length === 0 ? (
                <p>No products available</p>
            ) : (
                <div className="product-list grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                    {products.map((product) => (
                        <ProductCard key={product.id} product={product} />
                    ))}
                </div>
            )}
        </div>
    );
}

export default ProductList;
