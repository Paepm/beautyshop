import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";


export default function OrderDetail() {
    const { id } = useParams();  // aus URL: /orders/:id
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
                setProductItems(itemRes.data);  // <– richtige Produktinfos mit Namen/Bildern
            } catch (error) {
                console.error("Fehler beim Laden:", error);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, [id]);

    if (loading) return <p>Loading...</p>;
    if (!order) return <p>Order not found.</p>;

    return (
        <div className="max-w-3xl mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Order #{order.id}</h1>

            <div className="mb-4 space-y-1">
                <p><strong>Date:</strong> {new Date(order.created_at).toLocaleDateString()}</p>
                <p><strong>Status:</strong> {order.order_status}</p>
                <p><strong>Payment:</strong> {order.payment_provider} ({order.payment_method})</p>
                <p><strong>Shipping:</strong> {order.shipping_address}</p>
                <p><strong>Total:</strong> {order.total_price} €</p>
            </div>

            <h2 className="text-xl font-semibold mt-6 mb-2">Products</h2>
            <div className="space-y-3">
                {productItems.map((item, index) => (
                    <div key={index} className="p-3 border rounded shadow-sm">
                        <img src={item.product_image} alt={item.product_name} className="w-24 h-24 object-cover mb-2" />
                        <p><strong>Product:</strong> {item.product_name}</p>
                        <p><strong>Description:</strong> {item.product_description}</p>
                        <p><strong>Quantity:</strong> {item.quantity}</p>
                        <p><strong>Price:</strong> {item.price} €</p>
                    </div>
                ))}
            </div>
        </div>
    );
}
