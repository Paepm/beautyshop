import { useEffect, useState } from "react";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";

import api from "../services/api";

function RegisterPage() {
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password1: "",
        password2: "",
        first_name: "",
        last_name: "",
        date_of_birth: "",
        gender: "",
        country: "",
        city: "",
        post_code: "",
        address: "",
        phone_number: "",
        newsletter_opt_in: true,
        terms_accepted: false,
    });

    const [errors, setErrors] = useState({});
    const [success, setSuccess] = useState(null);
    const [countryList, setCountryList] = useState([]);
    const navigate = useNavigate();


    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        const newValue = type === "checkbox" ? checked : value;
        setFormData((prev) => ({ ...prev, [name]: newValue }));
    };

    useEffect(() => {
        const fetchCountries = async () => {
            try {
                const response = await api.get("accounts/countries/");
                setCountryList(response.data);
            } catch (error) {
                console.error("Error loading countries:", error);
            }
        };
        fetchCountries();
    }, []);


    const handleSubmit = async (e) => {
        const csrftoken = Cookies.get("csrftoken");
        e.preventDefault();
        try {
            const response = await api.post("accounts/sign_up/", formData, {
                headers: {
                    "X-CSRFToken": csrftoken,
                },
                withCredentials: true,
            });
            setSuccess("Check your email to verify your account.");
            navigate("/check_email");
            setErrors({});
        } catch (err) {
            if (err.response?.status === 400) {
                console.log("Validation errors:", err.response.data);
                setErrors(err.response.data);
            } else {
                alert("Something went wrong.");
            }
        }
    };

    return (
        <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded shadow">
            <h2 className="text-2xl font-bold mb-4">Create Your Account</h2>

            {success && (
                <div className="bg-green-100 text-green-800 p-2 rounded mb-4">
                    {success}
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
                {[
                    { label: "Username", name: "username", type: "text" },
                    { label: "Email", name: "email", type: "email" },
                    { label: "Password", name: "password1", type: "password" },
                    { label: "Confirm Password", name: "password2", type: "password" },
                    { label: "First Name", name: "first_name", type: "text" },
                    { label: "Last Name", name: "last_name", type: "text" },
                    { label: "Date of Birth", name: "date_of_birth", type: "date" },
                    { label: "City", name: "city", type: "text" },
                    { label: "Post Code", name: "post_code", type: "text" },
                    { label: "Address", name: "address", type: "text" },
                    { label: "Phone Number", name: "phone_number", type: "tel" },
                ].map(({ label, name, type }) => (
                    <div key={name}>
                        <label className="block font-semibold">{label}</label>
                        <input
                            type={type}
                            name={name}
                            value={formData[name]}
                            onChange={handleChange}
                            className={`w-full px-3 py-2 border rounded ${errors[name] ? "border-red-500" : ""}`}
                        />
                        {errors[name] && (
                            <p className="text-red-600 text-sm mt-1">
                                {Array.isArray(errors[name]) ? errors[name][0] : errors[name]}
                            </p>
                        )}
                    </div>
                ))}

                <div>
                    <label className="block font-semibold">Gender</label>
                    <select
                        name="gender"
                        value={formData.gender}
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
                    <label className="block font-semibold">Country</label>
                    <select
                        name="country"
                        value={formData.country}
                        onChange={handleChange}
                        className={`w-full px-3 py-2 border rounded ${errors.country ? "border-red-500" : ""}`}
                    >
                        <option value="">Select Country</option>
                        {countryList.map((c) => (
                            <option key={c.code} value={c.code}>
                                {c.name}
                            </option>
                        ))}
                    </select>
                    {errors.country && (
                        <p className="text-red-600 text-sm mt-1">
                            {Array.isArray(errors.country) ? errors.country[0] : errors.country}
                        </p>
                    )}
                </div>


                <div>
                    <label className="inline-flex items-center">
                        <input
                            type="checkbox"
                            name="newsletter_opt_in"
                            checked={formData.newsletter_opt_in}
                            onChange={handleChange}
                            className="form-checkbox h-5 w-5 text-black"
                        />
                        <span className="ml-2">Subscribe to newsletter</span>
                    </label>
                </div>
                <div>
                    <label className="inline-flex items-center">
                        <input
                            type="checkbox"
                            name="terms_accepted"
                            checked={formData.terms_accepted}
                            onChange={handleChange}
                            className="form-checkbox h-5 w-5 text-black"
                        />
                        <span className="ml-2">Accept Terms</span>
                    </label>
                </div>

                <button
                    type="submit"
                    className="w-full bg-black text-white py-2 rounded hover:bg-gray-800"
                >
                    Register
                </button>
            </form>
        </div>
    );
}

export default RegisterPage;
