import { useEffect, useState } from "react";
import axios from "../services/api";
import { useNavigate } from "react-router-dom";

function AdminOrdersPage() {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        fetchOrders();
    }, []);

    async function fetchOrders() {
        try {
            const response = await axios.get("/adminpanel/orders/");
            setOrders(response.data);
        } catch (error) {
            console.error("Error fetching orders:", error);
            alert("Could not load orders.");
        } finally {
            setLoading(false);
        }
    }

    if (loading) {
        return <div className="p-4 text-center">Loading orders...</div>;
    }

    return (
        <div className="max-w-6xl mx-auto p-4">
            <h1 className="text-2xl font-bold mb-6">Admin – All Orders</h1>

            {orders.length === 0 ? (
                <p>No orders found.</p>
            ) : (
                <div className="overflow-x-auto">
                    <table className="min-w-full table-auto border-collapse border border-gray-300">
                        <thead className="bg-gray-100">
                            <tr>
                                <th className="border p-2 text-left">Order ID</th>
                                <th className="border p-2 text-left">User</th>
                                <th className="border p-2 text-left">Total (€)</th>
                                <th className="border p-2 text-left">Status</th>
                                <th className="border p-2 text-left">Date</th>
                                <th className="border p-2">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {orders.map((order) => (
                                <tr key={order.id} className="border-t">
                                    <td className="border p-2">{order.id}</td>
                                    <td className="border p-2">{order.user_email}</td>
                                    <td className="border p-2">{order.total_price} €</td>
                                    <td className="border p-2">{order.payment_status}</td>
                                    <td className="border p-2">{new Date(order.created_at).toLocaleString()}</td>
                                    <td className="border p-2 text-center">
                                        <button
                                            className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700"
                                            onClick={() => navigate(`/admin/orders/${order.id}`)}
                                        >
                                            Details
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}

export default AdminOrdersPage;
