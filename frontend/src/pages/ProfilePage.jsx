import { useEffect, useState } from "react";
import api from "../services/api";
import Cookies from "js-cookie";

function ProfilePage() {
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchProfile = async () => {
        try {
            const response = await api.get("/accounts/profile/");
            setUserData(response.data);
        } catch (error) {
            console.error("Error fetching profile:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchProfile();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUserData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const csrftoken = Cookies.get("csrftoken");
        const updatedData = { ...userData };
        delete updatedData.profile_image;   // THIS NEEDS TO BE HANDLED TOMORROW! IMGS HANDLING IS NOT DONE YET!!!

        try {
            const response = await api.patch("/accounts/profile/", updatedData, {
                headers: {
                    "X-CSRFToken": csrftoken,
                },
                withCredentials: true,
            });
            alert("Changes saved successfully!");
            await fetchProfile(); // Reload latest data
        } catch (error) {
            console.error("Error saving profile:", error.response?.data || error);
            alert("Failed to save changes. Please try again.");
        }
    };

    if (loading || !userData) return <div>Loading...</div>;

    return (
        <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded shadow">
            <h2 className="text-2xl font-bold mb-4">My Profile</h2>
            <form className="space-y-4" onSubmit={handleSubmit}>
                {Object.entries(userData).map(([key, value]) => (
                    <div key={key}>
                        <label className="block font-semibold capitalize">
                            {key.replace(/_/g, " ")}
                        </label>
                        <input
                            type="text"
                            name={key}
                            value={value || ""}
                            onChange={handleChange}
                            className="w-full px-3 py-2 border rounded"
                            disabled={["id", "date_joined", "last_login"].includes(key)}
                        />
                    </div>
                ))}
                <button
                    type="submit"
                    className="w-full bg-black text-white py-2 rounded hover:bg-gray-800"
                >
                    Save Changes
                </button>
            </form>
        </div>
    );
}

export default ProfilePage;
