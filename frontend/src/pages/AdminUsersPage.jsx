import { useEffect, useState } from "react";
import api from "../services/api";
import { Link } from "react-router-dom";

function AdminUserPage() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchUsers();
    }, []);

    async function fetchUsers() {
        try {
            const response = await api.get("adminpanel/users/");
            setUsers(response.data);
        } catch (err) {
            console.error("Failed to fetch users:", err);
            setError("Failed to fetch users");
        } finally {
            setLoading(false);
        }
    }

    if (loading) return <div className="p-4">Loading users...</div>;
    if (error) return <div className="p-4 text-red-600">{error}</div>;

    return (
        <div className="max-w-5xl mx-auto p-4">
            <h1 className="text-2xl font-bold mb-6">Admin: User Overview</h1>

            <table className="w-full border rounded shadow">
                <thead>
                    <tr className="bg-gray-100 text-left">
                        <th className="p-2 border">ID</th>
                        <th className="p-2 border">Email</th>
                        <th className="p-2 border">First Name</th>
                        <th className="p-2 border">Last Name</th>
                        <th className="p-2 border">Is Superuser</th>
                        <th className="p-2 border">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map((user) => (
                        <tr key={user.id} className="hover:bg-gray-50">
                            <td className="p-2 border">{user.id}</td>
                            <td className="p-2 border">{user.email}</td>
                            <td className="p-2 border">{user.first_name}</td>
                            <td className="p-2 border">{user.last_name}</td>
                            <td className="p-2 border">{user.is_superuser ? "Yes" : "No"}</td>
                            <td className="p-2 border">
                                <Link to={`/admin/users/${user.id}`} className="text-blue-600 underline">
                                    View
                                </Link>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default AdminUserPage;
