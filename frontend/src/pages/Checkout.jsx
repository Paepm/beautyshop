import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Checkout() {
    const [cartItems, setCartItems] = useState([]);
    const [shippingAddress, setShippingAddress] = useState({
        "address": "",
        "city": "",
        "post_code": "",
        "country": ""
    });
    const [shippingMethod, setShippingMethod] = useState("standard");
    const [shippingCost, setShippingCost] = useState(4.9);
    const [subtotal, setSubtotal] = useState(0);
    const [agreedToTerms, setAgreedToTerms] = useState(false);
    const [countryList, setCountryList] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchCheckoutData();
    }, []);

    async function fetchCheckoutData() {
        const cartResponse = await api.get("cart/");
        const countryRes = await api.get("accounts/countries/");
        setCountryList(countryRes.data);
        setCartItems(cartResponse.data.items);
        setSubtotal(cartResponse.data.total_price);

        const profileResponse = await api.get("accounts/profile/");
        setShippingAddress({
            address: profileResponse.data.address,
            city: profileResponse.data.city,
            post_code: profileResponse.data.post_code,
            country: profileResponse.data.country
        });

    }

    function handleShippingChange(event) {
        const method = event.target.value;
        setShippingMethod(method);
        setShippingCost(method === "express" ? 9.9 : 4.9);
    }

    function handlePayment() {
        if (!agreedToTerms) {
            alert("Please Accept the GTC to proceed.");
            return;
        }
        // Weiterleitung zur Zahlungsseite oder API-Aufruf starten
        navigate("/payment");
    }

    const total = (parseFloat(subtotal) + parseFloat(shippingCost)).toFixed(2);

    return (
        <div className="max-w-4xl mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Continue to pay</h1>

            <section className="mb-6">
                <h2 className="text-xl font-semibold mb-2">Delivery Address</h2>

                <div className="border p-3 rounded space-y-2">
                    <label className="block text-sm font-medium mb-1">Street</label>
                    <input
                        type="text"
                        placeholder="Street and house number"
                        value={shippingAddress.address}
                        onChange={(e) =>
                            setShippingAddress({ ...shippingAddress, address: e.target.value })
                        }
                        className="w-full border px-2 py-1 rounded"
                    />
                    <div className="space-y-2">
                        <div>
                            <label className="block text-sm font-medium mb-1">Postal Code</label>
                            <input
                                type="text"
                                placeholder="ZIP"
                                value={shippingAddress.post_code}
                                onChange={(e) =>
                                    setShippingAddress({ ...shippingAddress, post_code: e.target.value })
                                }
                                className="w-full border px-2 py-1 rounded"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">City</label>
                            <input
                                type="text"
                                placeholder="City"
                                value={shippingAddress.city}
                                onChange={(e) =>
                                    setShippingAddress({ ...shippingAddress, city: e.target.value })
                                }
                                className="w-full border px-2 py-1 rounded"
                            />
                        </div>
                    </div>

                    <label className="block text-sm font-medium mb-1">Country</label>
                    <select
                        name="country"
                        value={shippingAddress.country || ""}
                        onChange={(e) =>
                            setShippingAddress({ ...shippingAddress, country: e.target.value })
                        }
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
            </section>


            <section className="mb-6">
                <h2 className="text-xl font-semibold mb-2">Products</h2>
                {cartItems.map((item) => (
                    <div key={item.id} className="flex justify-between py-1 border-b">
                        <span>{item.product.name} × {item.quantity}</span>
                        <span>{(item.quantity * item.product.price).toFixed(2)} €</span>
                    </div>
                ))}
                <div className="flex justify-between font-semibold mt-2">
                    <span>Subtotal</span>
                    <span>{subtotal.toFixed(2)} €</span>
                </div>
            </section>

            <section className="mb-6">
                <h2 className="text-xl font-semibold mb-2">Shipping method</h2>
                <div className="space-y-2">
                    <label className="flex items-center gap-2">
                        <input
                            type="radio"
                            name="shipping"
                            value="standard"
                            checked={shippingMethod === "standard"}
                            onChange={handleShippingChange}
                        />
                        Standard shipping (€4,90)
                    </label>
                    <label className="flex items-center gap-2">
                        <input
                            type="radio"
                            name="shipping"
                            value="express"
                            checked={shippingMethod === "express"}
                            onChange={handleShippingChange}
                        />
                        Express shipping (€9,90)
                    </label>
                </div>
            </section>

            <section className="mb-6">
                <div className="flex justify-between text-lg font-bold">
                    <span>Total Price</span>
                    <span>{total} €</span>
                </div>
            </section>

            <section className="mb-6">
                <label className="flex items-center gap-2">
                    <input
                        type="checkbox"
                        checked={agreedToTerms}
                        onChange={(e) => setAgreedToTerms(e.target.checked)}
                    />
                    I accept the <a href="/agb" className="text-blue-600">GTC</a>
                </label>
            </section>

            <button
                onClick={handlePayment}
                className="bg-black text-white px-6 py-3 rounded hover:bg-gray-800 disabled:opacity-50"
                disabled={!agreedToTerms}
            >
                pay now
            </button>
        </div>
    );
}

export default Checkout;
