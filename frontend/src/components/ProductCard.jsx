import Cookies from 'js-cookie';
import api from '../services/api';
import { AuthContext } from '../contexts/AuthContext';
import { useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';

import LoginPage from '../pages/LoginPage';

function ProductCard({ product }) {

    const { isAuthenticated } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleAddToCart = async () => {
        console.log("User is authenticated:", isAuthenticated);
        if (!isAuthenticated) {
            navigate('/login');
            return;
        }

        try {
            const csrfToken = Cookies.get('csrftoken');
            const formData = new URLSearchParams();
            formData.append('action', 'increment');
            formData.append('quantity', 1);
            console.log('➡️ Sende an:', `cart/add/${product.id}/`);
            await api.post(`cart/add/${product.id}/`, formData, {
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                responseType: 'json',
            });
            console.log("✅ Produkt hinzugefügt!");
            alert('Produkt wurde zum Warenkorb hinzugefügt!');
        } catch (error) {
            if (error.response) {
                console.error('❌ Axios Response Error:', error.response.status, error.response.data);
            } else if (error.request) {
                console.error('❌ Axios No Response:', error.request);
            } else {
                console.error('❌ Axios Error:', error.message);
            }
            alert('Fehler beim Hinzufügen zum Warenkorb.');
        }
    };


    return (
        <div className="border rounded-lg shadow-md p-4 flex flex-col items-center hover:shadow-lg transition">

            {/* Klickbarer Bereich für Detailseite */}
            <Link to={`/products/${product.id}`} className="w-full flex flex-col items-center no-underline text-black">
                <img
                    src={product.image}
                    alt={product.name}
                    className="w-48 h-48 object-cover mb-4"
                />
                <h2 className="text-lg font-semibold text-center">{product.name}</h2>
                <p className="text-gray-700 mb-2">{product.price} €</p>
            </Link>

            {/* Add-to-cart bleibt separat */}
            <button
                onClick={handleAddToCart}
                className="mt-auto bg-black text-white px-4 py-2 rounded hover:bg-gray-800 transition-colors"
            >
                add to cart
            </button>
        </div>
    );
}

export default ProductCard;
