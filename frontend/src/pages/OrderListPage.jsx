import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

import api from '../services/api';


function OrderList() {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        async function fetchOrders() {
            try {
                const response = await api.get('orders/orderlist/');
                setOrders(response.data);
                console.log("Fetched orders:", response.data);
            } catch (error) {
                console.error("Error fetching orders:", error);
            }
        }
        fetchOrders();
    }
        , []);


    return (
        <div className="max-w-4xl mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">My Orders</h1>

            {orders.length === 0 ? (
                <p>You do not have any orders yet.</p>
            ) : (
                <div className="space-y-4">
                    {orders.map((order) => (
                        <div
                            key={order.id}
                            className="border p-4 rounded shadow-sm hover:shadow-md transition"
                        >
                            <div className="flex justify-between items-center">
                                <div>
                                    <h2 className="font-semibold">Order #{order.id}</h2>
                                    <p className="text-sm text-gray-600">
                                        {new Date(order.created_at).toLocaleDateString()} – {order.payment_method}
                                    </p>
                                    <p className="mt-1 text-sm">
                                        Status: <strong>{order.status}</strong>
                                    </p>
                                </div>
                                <div className="text-right">
                                    <p className="font-bold">{order.total_price} €</p>
                                    <Link
                                        to={`/order_detail/${order.id}`}
                                        className="text-blue-600 hover:underline text-sm"
                                    >
                                        Show Details
                                    </Link>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
export default OrderList
