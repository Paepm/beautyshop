import { useContext, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";
import api from "../services/api";

function AdminOrdersDetailPage() {
    const { id } = useParams();
    const { user, isAuthenticated, loading } = useContext(AuthContext);
    const navigate = useNavigate();
    const [order, setOrder] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (loading) return;

        if (!isAuthenticated || !user?.is_superuser) {
            navigate("/");
            return;
        }

        const fetchOrder = async () => {
            try {
                const response = await api.get(`/adminpanel/orders/${id}/`);
                setOrder(response.data);
            } catch (err) {
                console.error("Failed to fetch order:", err);
                setError("Failed to fetch order details");
            }
        };

        fetchOrder();
    }, [id, isAuthenticated, user, loading, navigate]);

    if (loading || !user) return <p className="text-center mt-10">Loading...</p>;
    if (error) return <p className="text-center mt-10 text-red-500">{error}</p>;
    if (!order) return null;

    return (
        <div className="max-w-3xl mx-auto p-6">
            <h1 className="text-2xl font-bold mb-4">Order Detail (#{order.id})</h1>

            <div className="space-y-2">
                <p><strong>Username:</strong> {order.username}</p>
                <p><strong>User Email:</strong> {order.user?.email}</p>
                <p><strong>Order Status:</strong> {order.order_status}</p>
                <p><strong>Payment Status:</strong> {order.payment_status}</p>
                <p><strong>Payment Provider:</strong> {order.payment_provider}</p>
                <p><strong>Payment Method:</strong> {order.payment_method}</p>
                <p><strong>Total Price:</strong> €{order.total_price}</p>
                <p><strong>Created At:</strong> {new Date(order.created_at).toLocaleString()}</p>
            </div>

            <h2 className="text-xl font-semibold mt-6 mb-2">Shipping Information</h2>
            <div className="space-y-2">
                <p><strong>Address:</strong> {order.shipping_address}</p>
                <p><strong>City:</strong> {order.shipping_city}</p>
                <p><strong>Post Code:</strong> {order.shipping_post_code}</p>
                <p><strong>Country:</strong> {order.shipping_country}</p>
                <p><strong>Shipping Method:</strong> {order.shipping_method}</p>
                <p><strong>Shipping Cost:</strong> €{order.shipping_cost}</p>
            </div>

            <h2 className="text-xl font-semibold mt-6 mb-2">Items</h2>
            <ul className="space-y-2">
                {order.items?.map(item => (
                    <li key={item.id} className="border p-2 rounded">
                        {item.product?.name} × {item.quantity} — €{item.price}
                    </li>
                ))}
            </ul>
        </div>
    );

}

export default AdminOrdersDetailPage;
