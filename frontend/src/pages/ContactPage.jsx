import { useState } from "react";

const ContactPage = () => {
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        message: "",
    });

    const [submitted, setSubmitted] = useState(false);
    const [error, setError] = useState("");

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!formData.name || !formData.email || !formData.message) {
            setError("Please fill out all fields.");
            return;
        }

        try {
            // Hier wird später dein Backend angebunden:
            // await api.post("/contact/", formData);

            setSubmitted(true);
            setError("");
        } catch (err) {
            console.error("Error sending message:", err);
            setError("Something went wrong. Please try again.");
        }
    };

    return (
        <div className="max-w-xl mx-auto p-6">
            <h1 className="text-2xl font-bold mb-4">Contact Us</h1>

            {submitted ? (
                <div className="bg-green-100 border border-green-300 text-green-700 p-4 rounded">
                    Thank you! Your message has been sent.
                </div>
            ) : (
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block font-medium mb-1">Name</label>
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            className="w-full border px-3 py-2 rounded"
                            placeholder="Your name"
                        />
                    </div>
                    <div>
                        <label className="block font-medium mb-1">Email</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            className="w-full border px-3 py-2 rounded"
                            placeholder="you@example.com"
                        />
                    </div>
                    <div>
                        <label className="block font-medium mb-1">Message</label>
                        <textarea
                            name="message"
                            rows="5"
                            value={formData.message}
                            onChange={handleChange}
                            className="w-full border px-3 py-2 rounded"
                            placeholder="Your message"
                        />
                    </div>

                    {error && <p className="text-red-600">{error}</p>}

                    <button
                        type="submit"
                        className="bg-black text-white px-5 py-2 rounded hover:bg-gray-800"
                    >
                        Send Message
                    </button>
                </form>
            )}
        </div>
    );
};

export default ContactPage;
