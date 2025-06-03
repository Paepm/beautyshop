import React, { useEffect, useState, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";

import api from "../services/api";
import { AuthContext } from "../contexts/AuthContext";


const SuccessPage = () => {
    const { orderId } = useParams();
    const navigate = useNavigate();
    const [order, setOrder] = useState(null);
    const [loading, setLoading] = useState(true);
    const { isAuthenticated, loading: authLoading } = useContext(AuthContext);


    useEffect(() => {
        if (authLoading || !isAuthenticated) return;

        api
            .get(`orders/order_detail/${orderId}/`)
            .then((response) => {
                setOrder(response.data);
            })
            .catch((error) => {
                console.error("Order not found:", error);
                navigate("/");
            })
            .finally(() => {
                setLoading(false);
            });
    }, [authLoading, isAuthenticated, orderId, navigate]);


    if (loading) return <p className="text-center mt-10">Lade Bestellinformationen...</p>;
    if (!order) return <p className="text-center mt-10">Bestellung nicht gefunden.</p>;

    return (
        <div className="max-w-xl mx-auto text-center mt-10">
            <h1 className="text-3xl font-bold mb-4">Vielen Dank für deine Bestellung!</h1>
            <p className="text-lg mb-6">Bestellnummer: <strong>#{order.id}</strong></p>

            <div className="border p-4 rounded-xl shadow-lg text-left">
                <p>Status: <strong>{order.payment_status}</strong></p>
                <p>Gesamtbetrag: <strong>{(order.total_price / 100).toFixed(2)} €</strong></p>
                <p>Versandadresse: <br /> {order.shipping_address}</p>
            </div>

            <div className="mt-6">
                <a href="/" className="text-blue-600 hover:underline">Zurück zur Startseite</a>
            </div>
        </div>
    );
};

export default SuccessPage;
