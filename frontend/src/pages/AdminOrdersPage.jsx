import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { saveAs } from 'file-saver';
import { AuthContext } from "../contexts/AuthContext";
import api from '../services/api';


function AdminOrdersPage() {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filters, setFilters] = useState({
        username: '',
        payment_status: '',
        order_status: '',
        date_from: '',
        date_to: ''
    });
    const { user, isAuthenticated } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        if (!isAuthenticated || !user?.is_superuser) {
            navigate("/");
            return;
        }
        fetchOrders();
    }, [filters]);

    async function fetchOrders(filterParams = {}) {
        try {
            const response = await api.get("adminpanel/orders/", {
                params: filterParams
            });
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
            const params = {
                file_format: format,
                ...filters,
            };

            const response = await api.get('/adminpanel/orders/export/', {
                params,
                responseType: 'blob',
            });
            const now = new Date();
            const dateStr = now.toLocaleDateString("de-DE").replace(/\./g, "-");
            const timeStr = now.toLocaleTimeString("de-DE", {
                hour: "2-digit",
                minute: "2-digit",
                hour12: false,  // 24-Stunden-Format
            }).replace(":", "-");

            const filename = `${dateStr}_${timeStr}_orders.pdf`;

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

            {/* Export Buttons */}
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

            {/* Filter Controls */}
            <div className="flex flex-wrap gap-4 mb-6">
                <div className="flex flex-col">
                    <label className="mb-1 text-sm font-medium">Username</label>
                    <input
                        type="text"
                        name="username"
                        value={filters.username}
                        onChange={(e) => setFilters({ ...filters, username: e.target.value })}
                        className="border rounded px-3 py-2"
                        placeholder="e.g. admin"
                    />
                </div>
                <div className="flex flex-col">
                    <label className="mb-1 text-sm font-medium">Payment Status</label>
                    <select
                        name="payment_status"
                        value={filters.payment_status}
                        onChange={(e) => setFilters({ ...filters, payment_status: e.target.value })}
                        className="border rounded px-3 py-2"
                    >
                        <option value="">All Payment Status</option>
                        <option value="paid">Paid</option>
                        <option value="pending">Pending</option>
                        <option value="failed">Failed</option>
                    </select>
                </div>

                <div className="flex flex-col">
                    <label className="mb-1 text-sm font-medium">Order Status</label>
                    <select
                        name="order_status"
                        value={filters.order_status}
                        onChange={(e) => setFilters({ ...filters, order_status: e.target.value })}
                        className="border rounded px-3 py-2"
                    >
                        <option value="">All Order Status</option>
                        <option value="processing">Processing</option>
                        <option value="pending">Pending</option>
                        <option value="failed">Failed</option>
                    </select>
                </div>

                <div className="flex flex-col">
                    <label className="mb-1 text-sm font-medium">Date From</label>
                    <input
                        type="date"
                        name="date_from"
                        value={filters.date_from}
                        onChange={(e) => setFilters({ ...filters, date_from: e.target.value })}
                        className="border rounded px-3 py-2"
                    />
                </div>

                <div className="flex flex-col">
                    <label className="mb-1 text-sm font-medium">Date To</label>
                    <input
                        type="date"
                        name="date_to"
                        value={filters.date_to}
                        onChange={(e) => setFilters({ ...filters, date_to: e.target.value })}
                        className="border rounded px-3 py-2"
                    />
                </div>

                <button
                    className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded"
                    onClick={() => fetchOrders(filters)}
                >
                    Filter
                </button>
            </div>

            {/* Order Table */}
            {orders.length === 0 ? (
                <p>No orders found.</p>
            ) : (
                <div className="overflow-x-auto">
                    <table className="min-w-full table-auto border-collapse border border-gray-300">
                        <thead className="bg-gray-100">
                            <tr>
                                <th className="border p-2 text-left">Order ID</th>
                                <th className="border p-2 text-left">Username</th>
                                <th className="border p-2 text-left">Order Price (€)</th>
                                <th className="border p-2 text-left">Shipping Costs (€)</th>
                                <th className="border p-2 text-left">Total Price (€)</th>
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
                                    <td className="border p-2">{order.shipping_cost} €</td>
                                    <td className="border p-2">{(parseFloat(order.shipping_cost) + parseFloat(order.total_price)).toFixed(2)} €</td>
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
