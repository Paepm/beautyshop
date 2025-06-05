import { useEffect, useState } from "react";
import axios from "../services/api";
import { useNavigate } from "react-router-dom";
import { saveAs } from 'file-saver';
import api from '../services/api';

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

    const downloadFile = async (format) => {
        try {
            const response = await api.get(`/adminpanel/orders/export/?format=${format}´;
`, {
                responseType: 'blob',
            });

            const filename = `orders_export.${format}`;
            saveAs(response.data, filename);
        } catch (error) {
            console.error("Download failed:", error);
            alert("Fehler beim Herunterladen der Datei.");
        }
    };

    if (loading) {
        return <div className="p-4 text-center">Loading orders...</div>;
    }

    return (
        <div className="max-w-6xl mx-auto p-4">
            <h1 className="text-2xl font-bold mb-6">Admin – All Orders</h1>

            <div className="flex space-x-3 my-4">
                <button
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                    onClick={() => downloadFile("pdf")}
                >
                    📄 Export as PDF
                </button>
                <button
                    className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
                    onClick={() => downloadFile("csv")}
                >
                    📊 Export as CSV
                </button>
            </div>

            {orders.length === 0 ? (
                <p>No orders found.</p>
            ) : (
                <div className="overflow-x-auto">
                    <table className="min-w-full table-auto border-collapse border border-gray-300">
                        <thead className="bg-gray-100">
                            <tr>
                                <th className="border p-2 text-left">Order ID</th>
                                <th className="border p-2 text-left">Username</th>
                                <th className="border p-2 text-left">Total (€)</th>
                                <th className="border p-2 text-left">Payment Status</th>
                                <th className="border p-2 text-left">Order Status</th>
                                <th className="border p-2 text-left">Order Created Date</th>
                                <th className="border p-2">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {orders.map((order) => (
                                <tr key={order.id} className="border-t">
                                    <td className="border p-2">{order.id}</td>
                                    <td className="border p-2">{order.username}</td>
                                    <td className="border p-2">{order.total_price} €</td>
                                    <td className="border p-2">{order.payment_status}</td>
                                    <td className="border p-2">{order.order_status}</td>
                                    <td className="border p-2">{new Date(order.created_at).toLocaleString()}</td>
                                    <td className="border p-2 text-center">
                                        <button
                                            className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700"
                                            onClick={() => navigate(`/adminpanel/orders/${order.id}`)}
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
