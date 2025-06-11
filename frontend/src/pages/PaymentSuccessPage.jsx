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


    if (loading) return <p className="text-center mt-10">Download order information...</p>;
    if (!order) return <p className="text-center mt-10">Order not found.</p>;

    return (
        <div className="max-w-xl mx-auto text-center mt-10">
            <h1 className="text-3xl font-bold mb-4">Thank you for your order!</h1>

            <div className="border p-4 rounded-xl shadow-lg text-left">
                <h3>Your order will now be processed by us, you should receive a confirmation email on the email address you provided. Thank you for your trust and your purchase
                    Best regards your WohnSinn team</h3>
            </div>

            <div className="mt-6">
                <button>
                    <span className="bg-black text-white px-6 py-3 rounded hover:bg-gray-800 disabled:opacity-50" onClick={() => navigate("/")}>
                        Continue Shopping
                    </span>
                </button>
            </div>
        </div>
    );
};

export default SuccessPage;
