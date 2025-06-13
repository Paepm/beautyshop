import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../services/api";

export default function OrderDetail() {
    const { id } = useParams();
    const [order, setOrder] = useState(null);
    const [loading, setLoading] = useState(true);
    const [productItems, setProductItems] = useState([]);

    useEffect(() => {
        async function fetchData() {
            try {
                const [orderRes, itemRes] = await Promise.all([
                    api.get(`orders/order_detail/${id}/`),
                    api.get(`orders/order_product/${id}/`)
                ]);

                setOrder(orderRes.data);
                setProductItems(itemRes.data);
            } catch (error) {
                console.error("Fehler beim Laden:", error);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, [id]);

    if (loading) return <p className="text-center py-10">Loading...</p>;
    if (!order) return <p className="text-center py-10">Order not found.</p>;

    return (
        <div className="max-w-4xl mx-auto p-6 bg-white shadow rounded">
            <h1 className="text-2xl font-bold mb-6">Order #{order.id}</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8 text-sm text-gray-700">
                <div className="p-4 border rounded bg-gray-50">
                    <h2 className="font-semibold mb-2 text-gray-900">Order Information</h2>
                    <p><span className="font-medium">Date:</span> {new Date(order.created_at).toLocaleDateString()}</p>
                    <p><span className="font-medium">Status:</span> {order.order_status}</p>
                    <p><span className="font-medium">Total:</span> {order.total_price} €</p>
                </div>
                <div className="p-4 border rounded bg-gray-50">
                    <h2 className="font-semibold mb-2 text-gray-900">Payment & Shipping</h2>
                    <p><span className="font-medium">Payment:</span> {order.payment_method} ({order.payment_method})</p>
                    <p><span className="font-medium">Shipping:</span> {order.shipping_cost}</p>
                    <p><span className="font-medium">Address:</span> {order.shipping_address}</p>
                </div>
            </div>

            <h2 className="text-xl font-semibold mb-4">Products</h2>
            <div className="space-y-4">
                {productItems.map((item, index) => (
                    <div key={index} className="flex items-center gap-4 border rounded p-4 shadow-sm">
                        <img
                            src={item.product_image}
                            alt={item.product_name}
                            className="w-20 h-20 object-cover rounded"
                        />
                        <div className="flex-1">
                            <Link to={`/products/${item.product}`} className="hover:underline">
                                <p className="font-semibold">{item.product_name}</p>
                            </Link>
                            <p className="text-sm text-gray-600">Quantity: {item.quantity}</p>
                        </div>
                        <div className="text-right">
                            <p className="text-sm text-gray-600">Price/unit</p>
                            <p className="font-semibold">{parseFloat(item.price_current).toFixed(2)} €</p>
                            <p className="text-sm text-gray-600 mt-1">Total:</p>
                            <p className="font-medium">{(item.quantity * parseFloat(item.price_current)).toFixed(2)} €</p>

                        </div>
                    </div>
                ))}
            </div>

            <div className="mt-8 border-t pt-4 text-right text-lg font-bold">
                Total: {order.total_price} €
            </div>
        </div>
    );
}
