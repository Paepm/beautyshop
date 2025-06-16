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
    const [showModal, setShowModal] = useState(false);
    const [message, setMessage] = useState("");
    const [newOrderStatus, setNewOrderStatus] = useState("");
    const [newShippingProvider, setNewShippingProvider] = useState("");
    const [newTrackingId, setNewTrackingId] = useState("");
    const [newTrackingUrl, setNewTrackingUrl] = useState("");

    const [checkedItems, setCheckedItems] = useState({});

    // Modal: States aktualisieren beim Öffnen
    useEffect(() => {
        if (showModal && order) {
            setNewOrderStatus(order.order_status || "");
            setNewShippingProvider(order.shipping_provider || "");
            setNewTrackingId(order.tracking_id || "");
            setNewTrackingUrl(order.tracking_url || "");
        }
    }, [showModal, order]);

    // Hauptdaten laden
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

    const toggleChecked = (itemId) => {
        setCheckedItems((prev) => ({
            ...prev,
            [itemId]: !prev[itemId],
        }));
    };

    const handleStatusUpdate = async () => {
        try {
            await api.patch(`/adminpanel/orders_status_manager/${id}/`, {
                order_status: newOrderStatus,
                shipping_provider: newShippingProvider,
                tracking_id: newTrackingId,
                tracking_url: newTrackingUrl,
            });

            console.log({
                order_status: newOrderStatus,
                shipping_provider: newShippingProvider,
                tracking_id: newTrackingId,
                tracking_url: newTrackingUrl,
            });

            setMessage("✅ Status successfully updated.");
            setShowModal(false);

            // Order-Daten neu laden
            const response = await api.get(`/adminpanel/orders/${id}/`);
            setOrder(response.data);
        } catch (err) {
            console.error("Update failed:", err);
            setMessage("❌ Error by update Status.");
        }
    };

    if (loading || !user) return <p className="text-center mt-10">Loading...</p>;
    if (error) return <p className="text-center mt-10 text-red-500">{error}</p>;
    if (!order) return null;

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold">Order Detail (#{order.id})</h1>
                <button
                    className="mb-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                    onClick={() => setShowModal(true)}
                >
                    ✏️ Shipping and status handler
                </button>
            </div>

            {message && <p className="text-sm text-green-600">{message}</p>}

            {/* Ordered Items */}
            <div className="bg-white shadow-md rounded-lg p-5">
                <h2 className="text-xl font-semibold mb-4">🧴 Ordered Items</h2>
                <div className="overflow-x-auto">
                    <table className="min-w-full table-auto text-sm text-left text-gray-700">
                        <thead className="bg-gray-100 font-semibold">
                            <tr>
                                <th className="p-2">Product</th>
                                <th className="p-2">Article No.</th>
                                <th className="p-2 text-center">Qty</th>
                                <th className="p-2 text-center">Checked</th>
                            </tr>
                        </thead>
                        <tbody>
                            {order.items?.map((item) => (
                                <tr key={item.id} className="border-t hover:bg-gray-50">
                                    <td className="p-2">{item.product?.name}</td>
                                    <td className="p-2 font-mono text-xs text-gray-500">
                                        {item.product?.article_number || "—"}
                                    </td>
                                    <td className="p-2 text-center">{item.quantity}</td>
                                    <td className="p-2 text-center">
                                        <input
                                            type="checkbox"
                                            checked={checkedItems[item.id] || false}
                                            onChange={() => toggleChecked(item.id)}
                                            className="accent-green-600 w-4 h-4"
                                        />
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Shipping Info */}
            <div className="bg-white shadow-md rounded-lg p-5">
                <h2 className="text-xl font-semibold mb-3">🚚 Shipping Information</h2>
                <div className="grid grid-cols-2 gap-4">
                    <p><strong>First Name:</strong> {order.shipping_first_name}</p>
                    <p><strong>Last Name:</strong> {order.shipping_last_name}</p>
                    <p><strong>Address:</strong> {order.shipping_address}</p>
                    <p><strong>City:</strong> {order.shipping_city}</p>
                    <p><strong>Post Code:</strong> {order.shipping_post_code}</p>
                    <p><strong>Country:</strong> {order.shipping_country}</p>
                    <p><strong>Shipping Cost:</strong> €{order.shipping_cost}</p>
                </div>
            </div>

            {/* User Information */}
            <div className="bg-white shadow-md rounded-lg p-5">
                <h2 className="text-xl font-semibold mb-3">👤 User Information</h2>
                <p><strong>Username:</strong> {order.username}</p>
                <p><strong>User Email:</strong> {order.user?.email}</p>
            </div>

            {/* Order Details */}
            <div className="bg-white shadow-md rounded-lg p-5">
                <h2 className="text-xl font-semibold mb-3">🧾 Order Details</h2>
                <div className="grid grid-cols-2 gap-4">
                    <p><strong>Order Status:</strong> {order.order_status}</p>
                    <p><strong>Payment Status:</strong> {order.payment_status}</p>
                    <p><strong>Payment Provider:</strong> {order.payment_provider}</p>
                    <p><strong>Payment Method:</strong> {order.payment_method}</p>
                    <p><strong>Total Price:</strong> €{order.total_price}</p>
                    <p><strong>Created At:</strong> {new Date(order.created_at).toLocaleString()}</p>
                </div>
            </div>

            {/* MODAL */}
            {showModal && (
                <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
                    <div className="bg-white p-6 rounded shadow-lg w-full max-w-md">
                        <h2 className="text-xl font-semibold mb-4">Change Status</h2>

                        <div className="mb-4">
                            <label className="block text-sm font-medium mb-1">Order Status</label>
                            <select
                                className="w-full border px-3 py-2 rounded"
                                value={newOrderStatus}
                                onChange={(e) => setNewOrderStatus(e.target.value)}
                            >
                                <option value="pending">Pending</option>
                                <option value="processing">Processing</option>
                                <option value="shipped">Shipped</option>
                                <option value="delivered">Delivered</option>
                                <option value="cancelled">Cancelled</option>
                            </select>
                        </div>

                        <div className="mb-4">
                            <label className="block text-sm font-medium mb-1">Shipping Provider</label>
                            <select
                                className="w-full border px-3 py-2 rounded"
                                value={newShippingProvider}
                                onChange={(e) => setNewShippingProvider(e.target.value)}
                            >
                                <option value="DPD">DPD</option>
                                <option value="Post AT">Post AT</option>
                            </select>
                        </div>

                        <div className="mb-4">
                            <label className="block text-sm font-medium mb-1">Tracking ID</label>
                            <input
                                type="text"
                                className="w-full border px-3 py-2 rounded"
                                value={newTrackingId}
                                onChange={(e) => setNewTrackingId(e.target.value)}
                            />
                        </div>

                        <div className="mb-4">
                            <label className="block text-sm font-medium mb-1">Tracking URL</label>
                            <input
                                type="text"
                                className="w-full border px-3 py-2 rounded"
                                value={newTrackingUrl}
                                onChange={(e) => setNewTrackingUrl(e.target.value)}
                            />
                        </div>

                        <div className="flex justify-end gap-2">
                            <button
                                className="px-4 py-2 rounded bg-gray-300 hover:bg-gray-400"
                                onClick={() => setShowModal(false)}
                            >
                                Cancel
                            </button>
                            <button
                                className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
                                onClick={handleStatusUpdate}
                            >
                                Save
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default AdminOrdersDetailPage;
