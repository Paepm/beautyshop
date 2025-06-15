import { useEffect, useState } from 'react';
import { useSearchParams, useLocation, useNavigate } from 'react-router-dom';
import api from '../services/api';
import ProductCard from './ProductCard';

function ProductList() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filterSale, setFilterSale] = useState(false);
    const [filterIsAvailable, setFilterIsAvailable] = useState(false);

    const [searchParams] = useSearchParams();
    const category = searchParams.get("category") || "";
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProducts = async () => {
            setLoading(true);
            try {
                const params = new URLSearchParams(location.search);
                const category = params.get("category") || '';
                const sale = params.get("sale") === "true";
                const available = params.get("available") === "true";
                const search = params.get("search") || '';

                setFilterSale(sale);
                setFilterIsAvailable(available);

                const requestParams = new URLSearchParams();
                if (category) requestParams.append("category", category);
                if (sale) requestParams.append("sale", "true");
                if (available) requestParams.append("available", "true");
                if (search) requestParams.append("search", search);

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
    }, [location.search]);

    const updateFilterParam = (key, value) => {
        const params = new URLSearchParams(location.search);
        if (value) {
            params.set(key, "true");
        } else {
            params.delete(key);
        }
        navigate({ search: params.toString() });
    };

    return (
        <div className="product-list-wrapper px-4">

            {/* Checkbox-Filter */}
            <div className="mb-4 flex items-center gap-6 flex-wrap text-sm">
                <label className="flex items-center gap-2">
                    <input
                        type="checkbox"
                        checked={filterSale}
                        onChange={(e) => updateFilterParam("sale", e.target.checked)}
                        className="form-checkbox"
                    />

                    show offers only
                </label>
                <label className="flex items-center gap-2">
                    <input
                        type="checkbox"
                        checked={filterIsAvailable}
                        onChange={(e) => updateFilterParam("available", e.target.checked)}
                        className="form-checkbox"
                    />

                    is available
                </label>
            </div>

            {/* Productlist */}
            {loading ? (
                <p>Loading products…</p>
            ) : products.length === 0 ? (
                <div className="p-6 text-center text-gray-500">
                    <p>No products found.</p>
                    <p className="text-sm">Try adjusting your filters or search terms.</p>
                </div>
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
