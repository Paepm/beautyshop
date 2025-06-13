import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

// ✅ Wiederverwendbares Passwortfeld mit Augensymbol
function PasswordInput({ label, name, value, onChange, error }) {
    const [showPassword, setShowPassword] = useState(false);

    return (
        <div className="relative">
            <label className="block font-semibold mb-1">{label}</label>
            <input
                type={showPassword ? "text" : "password"}
                name={name}
                value={value}
                onChange={onChange}
                className={`w-full px-3 py-2 border rounded pr-10 ${error ? "border-red-500" : ""}`}
            />
            <span
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-[42px] cursor-pointer text-gray-600 text-sm select-none"
                title={showPassword ? "Hide password" : "Show password"}
            >
                {showPassword ? "🙈" : "👁"}
            </span>
            {error && (
                <p className="text-red-600 text-sm mt-1">
                    {Array.isArray(error) ? error[0] : error}
                </p>
            )}
        </div>
    );
}

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

    const allowedCountries = ["AT", "DE", "LI", "CH"];

    useEffect(() => {
        const fetchCountries = async () => {
            try {
                const response = await api.get("accounts/countries/");
                const filtered = response.data.filter((c) =>
                    allowedCountries.includes(c.code)
                );
                setCountryList(filtered);
            } catch (error) {
                console.error("Error loading countries:", error);
            }
        };
        fetchCountries();
    }, []);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        const newValue = type === "checkbox" ? checked : value;
        setFormData((prev) => ({ ...prev, [name]: newValue }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post("accounts/sign_up/", formData);
            setSuccess("Check your email to verify your account.");
            setErrors({});
            navigate("/check_email");
        } catch (err) {
            if (err.response?.status === 400) {
                setErrors(err.response.data);
            } else {
                alert("Something went wrong.");
            }
        }
    };

    return (
        <div className="max-w-6xl mx-auto mt-10 p-6 bg-white rounded shadow">
            <h1 className="text-2xl font-bold mb-4">Create Your Account</h1>

            {success && (
                <div className="bg-green-100 text-green-800 p-2 rounded mb-4">
                    {success}
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Username and Email */}
                    <div>
                        <label className="block font-semibold mb-1">Username</label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            className={`w-full px-3 py-2 border rounded ${errors.username ? "border-red-500" : ""}`}
                        />
                        {errors.username && <p className="text-red-600 text-sm">{errors.username}</p>}
                    </div>

                    <div className="md:col-span-2">
                        <label className="block font-semibold mb-1">Email</label>
                        <input
                            type="email"
                            name="email"
                            placeholder="maxmustermann@test.at"
                            value={formData.email}
                            onChange={handleChange}
                            className={`w-full px-3 py-2 border rounded ${errors.email ? "border-red-500" : ""}`}
                        />
                        {errors.email && <p className="text-red-600 text-sm">{errors.email}</p>}
                    </div>

                    {/* Personal Info */}
                    <div>
                        <label className="block font-semibold mb-1">First Name</label>
                        <input type="text" name="first_name" value={formData.first_name} onChange={handleChange} className="w-full px-3 py-2 border rounded" />
                    </div>
                    <div>
                        <label className="block font-semibold mb-1">Last Name</label>
                        <input type="text" name="last_name" value={formData.last_name} onChange={handleChange} className="w-full px-3 py-2 border rounded" />
                    </div>
                    <div>
                        <label className="block font-semibold mb-1">Phone Number</label>
                        <input type="tel" name="phone_number" placeholder="optional" value={formData.phone_number} onChange={handleChange} className="w-full px-3 py-2 border rounded" />
                    </div>

                    {/* Address Info */}
                    <div>
                        <label className="block font-semibold mb-1">City</label>
                        <input type="text" name="city" placeholder="optional" value={formData.city} onChange={handleChange} className="w-full px-3 py-2 border rounded" />
                    </div>
                    <div>
                        <label className="block font-semibold mb-1">Post Code</label>
                        <input type="text" name="post_code" placeholder="optional" value={formData.post_code} onChange={handleChange} className="w-full px-3 py-2 border rounded" />
                    </div>
                    <div>
                        <label className="block font-semibold mb-1">Address</label>
                        <input type="text" name="address" placeholder="optional" value={formData.address} onChange={handleChange} className="w-full px-3 py-2 border rounded" />
                    </div>

                    {/* Date and Gender */}
                    <div>
                        <label className="block font-semibold mb-1">Date of Birth</label>
                        <input type="date" name="date_of_birth" value={formData.date_of_birth} onChange={handleChange} className="w-full px-3 py-2 border rounded" />
                    </div>
                    <div>
                        <label className="block font-semibold mb-1">Gender</label>
                        <select name="gender" value={formData.gender} onChange={handleChange} className="w-full px-3 py-2 border rounded">
                            <option value="">Select Gender</option>
                            <option value="M">Male</option>
                            <option value="F">Female</option>
                            <option value="D">Diverse</option>
                        </select>
                    </div>

                    {/* Country Selector (gefiltert) */}
                    <div>
                        <label className="block font-semibold mb-1">Country</label>
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
                        {errors.country && <p className="text-red-600 text-sm">{errors.country}</p>}
                    </div>

                    {/* Passwords */}
                    <PasswordInput label="Password" name="password1" value={formData.password1} onChange={handleChange} error={errors.password1} />
                    <PasswordInput label="Confirm Password" name="password2" value={formData.password2} onChange={handleChange} error={errors.password2} />

                    {/* Options */}
                    <div className="md:col-span-3 flex flex-col md:flex-row gap-6 mt-4">
                        <label className="inline-flex items-center">
                            <input type="checkbox" name="newsletter_opt_in" checked={formData.newsletter_opt_in} onChange={handleChange} className="form-checkbox h-5 w-5 text-black" />
                            <span className="ml-2">Subscribe to newsletter</span>
                        </label>
                        <label className="inline-flex items-center">
                            <input type="checkbox" name="terms_accepted" checked={formData.terms_accepted} onChange={handleChange} className="form-checkbox h-5 w-5 text-black" />
                            <span className="ml-2">Accept Terms</span>
                        </label>
                    </div>
                </div>

                <div className="flex justify-center">
                    <button type="submit" className="bg-black text-white px-6 py-2 rounded hover:bg-gray-800">
                        Register
                    </button>
                </div>
            </form>
        </div>
    );
}

export default RegisterPage;
