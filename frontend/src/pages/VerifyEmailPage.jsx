// src/pages/VerifyEmailPage.jsx
import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";

function VerifyEmailPage() {
    const { token } = useParams();
    const navigate = useNavigate();
    const [status, setStatus] = useState("pending");
    const [message, setMessage] = useState("");

    useEffect(() => {
        const verify = async () => {
            try {
                const response = await api.get(`accounts/verify/${token}/`);
                setStatus("success");
                setMessage(response.data.message || "Email verified.");
                setTimeout(() => navigate("/login"), 1000);
            } catch (err) {
                setStatus("error");
                if (err.response?.data?.message) {
                    setMessage(err.response.data.message);
                } else {
                    setMessage("Verification failed. Please try again later.");
                }
            }
        };
        verify();
    }, [token, navigate]);

    return (
        <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded shadow">
            <h2 className="text-2xl font-bold mb-4">Email Verification</h2>
            {status === "pending" && <p className="animate-pulse">Verifying your email...</p>}
            {status === "success" && <p className="text-green-600">{message}</p>}
            {status === "error" && <p className="text-red-600">{message}</p>}
        </div>
    );
}

export default VerifyEmailPage;
