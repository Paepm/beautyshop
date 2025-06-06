import { useState } from "react";
import api from "../services/api";

function AdminOrderStatusPage() {
    const [orderId, setOrderId] = useState("");
    const [message, setMessage] = useState("");
    const [newOrderStatus, setNewOrderStatus] = useState("");
    const [newPaymentStatus, setNewPaymentStatus] = useState("");



    const handleStatusChange = async () => {
        try {
            const response = await api.patch(`/adminpanel/orders_status_manager/${orderId}/`, {
                order_status: newOrderStatus,
                payment_status: newPaymentStatus,
            });
            setMessage(`✅ Order #${orderId} status updated successfully.`);
        } catch (error) {
            console.error("Error updating status:", error);
            setMessage("❌ Failed to update order status.");
        }
    };



    return (
        <div className="max-w-xl mx-auto p-4">
            <h1 className="text-2xl font-bold mb-6">Admin – Update Order Status</h1>

            <div className="mb-4">
                <label className="block mb-1 text-sm font-medium">Order ID</label>
                <input
                    type="text"
                    value={orderId}
                    onChange={(e) => setOrderId(e.target.value)}
                    className="w-full border px-3 py-2 rounded"
                    placeholder="Enter Order ID"
                />
            </div>

            <div className="mb-4">
                <label className="block mb-1 text-sm font-medium">Order Status</label>
                <select
                    value={newOrderStatus}
                    onChange={(e) => setNewOrderStatus(e.target.value)}
                    className="w-full border px-3 py-2 rounded"
                >

                    <option value="pending">Pending</option>
                    <option value="processing">Processing</option>
                    <option value="shipped">Shipped</option>
                    <option value="delivered">Delivered</option>
                    <option value="cancelled">Cancelled</option>
                </select>
            </div>

            <div className="mb-4">
                <label className="block mb-1 text-sm font-medium">Payment Status</label>
                <select
                    value={newPaymentStatus}
                    onChange={(e) => setNewPaymentStatus(e.target.value)}
                    className="w-full border px-3 py-2 rounded"
                >

                    <option value="open">Open</option>
                    <option value="paid">Paid</option>
                    <option value="failed">Failed</option>
                    <option value="expired">Expired</option>
                    <option value="processing">Processing</option>
                </select>
            </div>

            <button
                onClick={handleStatusChange}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
                Update Status
            </button>

            {message && <p className="mt-4 text-sm">{message}</p>}
        </div>
    );
}

export default AdminOrderStatusPage;
