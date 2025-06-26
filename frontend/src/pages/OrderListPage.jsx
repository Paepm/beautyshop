import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

import api, {baseUrl} from '../services/api';


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
                <div className="flex flex-col items-center justify-center text-center py-20 px-4 bg-gray-100 rounded">
                    <img
                        src="/media/shop_page/cart_img.png"
                        alt="Empty Cart"
                        className="w-20 h-20 mb-4"
                    />
                    <h2 className="text-2xl font-bold mb-2">Your Orderlist is empty.</h2>
                    <p className="text-gray-600 mb-6 max-w-md">
                        Browse our wide range of furniture and find your new favorites for every room.
                    </p>
                    <a
                        href="/productlist"
                        className="inline-block px-6 py-2 bg-black text-white rounded hover:bg-gray-800 transition"
                    >
                        Go to Products
                    </a>
                </div>
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
                                        Payment Status: <strong>{order.payment_status}</strong>
                                    </p>
                                    <p className="mt-1 text-sm">
                                        Payment Method: <strong>{order.payment_method}</strong>
                                    </p>
                                    <p className="mt-1 text-sm">
                                        Order Status: <strong>{order.order_status}</strong>
                                    </p>
                                </div>
                                <div className="text-right">
                                    <p className="font-bold">{order.total_price} €</p>
                                    <Link
                                        to={`/order_detail/${order.id}`}
                                        className="inline-block px-3 py-1 bg-black text-white rounded hover:bg-gray-800 transition"
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
