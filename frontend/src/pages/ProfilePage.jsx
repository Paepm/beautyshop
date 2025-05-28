import { useEffect, useState } from "react";
import api from "../services/api";
import Cookies from "js-cookie";

function ProfilePage() {
    const [userData, setUserData] = useState(null);
    const [countryList, setCountryList] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            try {
                const profileRes = await api.get("accounts/profile/");
                const countryRes = await api.get("accounts/countries/");
                setUserData(profileRes.data);
                setCountryList(countryRes.data);
            } catch (err) {
                console.error("Error loading data:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUserData((prev) => ({ ...prev, [name]: value }));
    };

    const handleDateChange = (e) => {
        setUserData((prev) => ({ ...prev, date_of_birth: e.target.value }));
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setUserData((prev) => ({ ...prev, profile_image: file }));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const csrftoken = Cookies.get("csrftoken");
        const form = new FormData();

        Object.entries(userData).forEach(([key, value]) => {
            if (key === "profile_image") {
                if (value instanceof File) {
                    form.append("profile_image", value);
                }
                // Falls kein neues Bild: nichts senden
            } else {
                form.append(key, value || "");
            }
        });

        try {
            await api.patch("accounts/profile/", form, {
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "multipart/form-data",
                },
                withCredentials: true,
            });
            alert("Changes saved successfully!");
            setError({}); // Reset errors on successful save
            console.log("Set errors state: cleared");
        } catch (err) {
            if (err.response?.status === 400) {
                console.log("Error object:", error);
                setError(err.response.data); // korrekt!
            } else {
                alert("Failed to save changes.");
            }
            console.error("Error saving profile:");
        }
    };

    if (loading || !userData) return <div>Loading...</div>;

    return (
        <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded shadow">
            <h2 className="text-2xl font-bold mb-4">Hello {userData.username}</h2>
            <h3 className="text-1xl font-bold mb-4">You can edit all fields here</h3>
            <form className="space-y-4" onSubmit={handleSubmit}>
                {/* ✅ LIVEDebug zeigt Fehler-Objekt live */}
                {Object.keys(error).length > 0 && (
                    <div className="bg-red-100 text-red-800 text-sm p-2 rounded mb-4">
                        <pre>{JSON.stringify(error, null, 2)}</pre>
                    </div>
                )}
                <div>
                    <label className="block font-semibold">First Name</label>
                    <input
                        type="text"
                        name="first_name"
                        value={userData.first_name || ""}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded"
                    />
                </div>
                <div>
                    <label className="block font-semibold">Last Name</label>
                    <input
                        type="text"
                        name="last_name"
                        value={userData.last_name || ""}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded"
                    />
                </div>
                <div>
                    <label className="block font-semibold">Profile Image</label>
                    <input
                        type="file"
                        name="profile_image"
                        accept="image/*"
                        onChange={handleFileChange}
                        className="w-full px-3 py-2 border rounded"
                    />
                    {userData.profile_image && !(userData.profile_image instanceof File) && (
                        <img
                            src={userData.profile_image}
                            alt="Profile"
                            className="mt-2 h-24 w-24 rounded object-cover"
                        />
                    )}
                </div>
                <div>
                    <label className="block font-semibold">Email</label>
                    <input
                        type="email"
                        name="email"
                        value={userData.email || ""}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded"
                    />
                </div>
                <div>
                    <label className="block font-semibold">Gender</label>
                    <select
                        name="gender"
                        value={userData.gender || ""}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded"
                    >
                        <option value="">Select Gender</option>
                        <option value="M">Male</option>
                        <option value="F">Female</option>
                        <option value="D">Diverse</option>
                    </select>
                </div>
                <div>
                    <label className="block font-semibold">Date of Birth</label>
                    <input
                        type="date"
                        name="date_of_birth"
                        value={userData.date_of_birth || ""}
                        onChange={handleDateChange}
                        className="w-full px-3 py-2 border rounded"
                    />
                </div>
                <div>
                    <label className="block font-semibold">Country</label>
                    <select
                        name="country"
                        value={userData.country || ""}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded"
                    >
                        <option value="">Select Country</option>
                        {countryList.map((c) => (
                            <option key={c.code} value={c.code}>
                                {c.name}
                            </option>
                        ))}
                    </select>
                </div>
                <div><label className="block font-semibold">City</label>
                    <input
                        type="city"
                        name="city"
                        value={userData.city || ""}
                        onChange={handleChange}
                        className={`w-full px-3 py-2 border rounded ${error.city ? "border-red-500" : ""
                            }`}
                    />
                    {error.city && (
                        <p className="text-red-600 text-sm mt-1">
                            {Array.isArray(error.city)
                                ? error.city[0]
                                : error.city}
                        </p>
                    )}
                </div>
                <div><label className="block font-semibold">Post Code</label>
                    <input
                        type="post_code"
                        name="post_code"
                        value={userData.post_code || ""}
                        onChange={handleChange}
                        className={`w-full px-3 py-2 border rounded ${error.post_code ? "border-red-500" : ""
                            }`}
                    />
                    {error.post_code && (
                        <p className="text-red-600 text-sm mt-1">
                            {Array.isArray(error.post_code)
                                ? error.post_code[0]
                                : error.post_code}
                        </p>
                    )}
                </div>
                <div><label className="block font-semibold">Address</label>
                    <input
                        type="address"
                        name="address"
                        value={userData.address || ""}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border rounded"
                    />
                </div>
                <div className="mb-4">
                    <label className="block font-semibold">Phone</label>
                    <input
                        type="tel"
                        name="phone_number"
                        value={userData.phone_number || ""}
                        onChange={handleChange}
                        className={`w-full px-3 py-2 border rounded ${error.phone_number ? "border-red-500" : ""
                            }`}
                    />
                    {error.phone_number && (
                        <p className="text-red-600 text-sm mt-1">
                            {Array.isArray(error.phone_number)
                                ? error.phone_number[0]
                                : error.phone_number}
                        </p>
                    )}
                </div>
                <div><label className="inline-flex items-center">
                    <input
                        type="checkbox"
                        name="newsletter_opt_in"
                        checked={userData.newsletter_opt_in || false}
                        onChange={(e) =>
                            setUserData((prev) => ({
                                ...prev,
                                newsletter_opt_in: e.target.checked,
                            }))
                        }
                        className="form-checkbox h-5 w-5 text-black"
                    />
                    <span className="ml-2">Subscribe to newsletter</span>
                </label></div>

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
