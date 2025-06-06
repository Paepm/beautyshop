import { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from '../contexts/AuthContext';


function AdminPanelPage() {
    const { user, isAuthenticated, loading } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        if (!loading) {
            if (!isAuthenticated || !user?.is_superuser) {
                navigate("/");  // Weiterleitung wenn kein Superuser
            }
        }
    }, [isAuthenticated, user, loading, navigate]);

    if (loading || !user) {
        return <p className="text-center mt-10">Loading...</p>;
    }

    return (
        <div className="max-w-3xl mx-auto p-6">
            <h1 className="text-2xl font-bold mb-4">Admin Panel</h1>

            <ul className="space-y-3">
                <li>
                    <button
                        onClick={() => navigate("/adminpanel/orders")}
                        className="w-full text-left px-4 py-2 border rounded hover:bg-gray-100"
                    >
                        🧾 All Orders
                    </button>
                </li>
                <li>
                    <button
                        onClick={() => navigate("/adminpanel/users")}
                        className="w-full text-left px-4 py-2 border rounded hover:bg-gray-100"
                    >
                        👥 All Users
                    </button>
                </li>
                <li>
                    <button
                        onClick={() => navigate("/adminpanel/order_status_manager")}
                        className="w-full text-left px-4 py-2 border rounded hover:bg-gray-100"
                    >
                        🚚 Order Status Management
                    </button>
                </li>
            </ul>
        </div>
    );
}

export default AdminPanelPage;
