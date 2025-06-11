import React, { useEffect, useState } from 'react';
import { useSearchParams, useLocation } from 'react-router-dom';
import api from '../services/api';
import ProductCard from './ProductCard';

function ProductList() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filterSale, setFilterSale] = useState(false);
    const [filterIsAvailable, setFilterIsAvailable] = useState(false);

    const [searchParams] = useSearchParams();
    const category = searchParams.get("category") || "";
    const [searchTerm, setSearchTerm] = useState("");
    const location = useLocation();

    useEffect(() => {
        const fetchProducts = async () => {
            setLoading(true);
            try {
                const params = new URLSearchParams(location.search);
                const category = params.get("category") || '';
                const search = params.get("search") || '';
                const sale = params.get("sale") === "true";
                const available = params.get("available") === "true";

                setSearchTerm(search);
                setFilterSale(sale);
                setFilterIsAvailable(available);

                const requestParams = new URLSearchParams();
                if (category) requestParams.append("category", category);
                if (search) requestParams.append("search", search);
                if (sale) requestParams.append("sale", "true");
                if (available) requestParams.append("available", "true");

                const url = requestParams.toString()
                    ? `products/?${requestParams.toString()}`
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
    }, [category, filterSale, filterIsAvailable, location.search]);

    return (
        <div className="product-list-wrapper px-4">

            {/* Checkbox-Filter */}
            <div className="mb-4 flex items-center gap-6 flex-wrap text-sm">
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
                    <input
                        type="checkbox"
                        checked={filterIsAvailable}
                        onChange={(e) => setFilterIsAvailable(e.target.checked)}
                        className="form-checkbox"
                    />
                    is available
                </label>
            </div>

            {/* Produktliste */}
            {loading ? (
                <p>Loading products…</p>
            ) : products.length === 0 ? (
                <p>No products available</p>
            ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                    {products.map((product) => (
                        <ProductCard key={product.id} product={product} />
                    ))}
                </div>
            )}
        </div>
    );
}

export default ProductList;
