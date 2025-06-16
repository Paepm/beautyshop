import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";


import api from "../services/api";
import { checkoutOrder } from "../services/orderService";

function Checkout() {
    const [cartItems, setCartItems] = useState([]);
    const [shippingAddress, setShippingAddress] = useState({
        first_name: "",
        last_name: "",
        address: "",
        city: "",
        post_code: "",
        country: ""
    });
    const [invoiceAddress, setInvoiceAddress] = useState({
        first_name: "",
        last_name: "",
        address: "",
        city: "",
        post_code: "",
        country: ""
    });
    const [showShippingFields, setShowShippingFields] = useState(false);
    const [shippingMethod, setShippingMethod] = useState("standard");
    const [shippingCost, setShippingCost] = useState(4.9);
    const [subtotal, setSubtotal] = useState(0);
    const [agreedToTerms, setAgreedToTerms] = useState(false);
    const [countryList, setCountryList] = useState([]);
    const [selectedPaymentMethod, setSelectedPaymentMethod] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const allowedCountries = ["AT", "DE", "LI", "CH"];


    useEffect(() => {
        fetchCheckoutData();
    }, []);

    async function fetchCheckoutData() {
        try {
            const cartResponse = await api.get("cart/");
            const countryRes = await api.get("accounts/countries/");
            const profileResponse = await api.get("accounts/profile/");

            const filtered = countryRes.data.filter((c) => allowedCountries.includes(c.code));
            setCountryList(filtered);
            setCartItems(cartResponse.data.items);
            setSubtotal(cartResponse.data.total_price);

            setShippingAddress({
                first_name: profileResponse.data.first_name,
                last_name: profileResponse.data.last_name,
                address: profileResponse.data.address,
                city: profileResponse.data.city,
                post_code: profileResponse.data.post_code,
                country: profileResponse.data.country
            });
            setInvoiceAddress({
                first_name: profileResponse.data.first_name,
                last_name: profileResponse.data.last_name,
                address: profileResponse.data.address,
                city: profileResponse.data.city,
                post_code: profileResponse.data.post_code,
                country: profileResponse.data.country
            });

        } catch (err) {
            console.error("Error during loading checkout datas", err);
            const errorDetail = err.response?.data?.detail || "Something went wrong. Please try again.";
            setErrorMessage(errorDetail);
        }
    }

    function handleShippingChange(event) {
        const method = event.target.value;
        setShippingMethod(method);
        setShippingCost(method === "express" ? 9.9 : 4.9);
    }

    async function handlePayment() {
        if (!agreedToTerms) {
            alert("Please Accept the GTC to proceed.");
            return;
        }

        if (!selectedPaymentMethod) {
            alert("Please select a payment method.");
            return;
        }

        try {
            const payload = {
                invoice_data: invoiceAddress,
                shipping_data: showShippingFields ? shippingAddress : invoiceAddress,
                shipping_method: shippingMethod,
                payment_provider: selectedPaymentMethod === "paypal" ? "paypal" : "stripe",
                payment_method: selectedPaymentMethod
            };


            const response = await checkoutOrder(payload);
            const redirectUrl = response.data.redirect_url;
            window.location.href = redirectUrl;

        } catch (err) {
            console.error("Fehler beim Checkout:", err);
            alert("Something went wrong. Please try again.");
        }
    }

    const total = (parseFloat(subtotal) + parseFloat(shippingCost)).toFixed(2);

    return (
        <div className="max-w-4xl mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Continue to pay</h1>

            <section className="mb-6">
                <h2 className="text-xl font-semibold mb-4">Products</h2>

                {/* Tabellenkopf */}
                <div className="hidden md:grid grid-cols-12 gap-4 font-semibold text-sm border-b pb-2 mb-2">
                    <div className="col-span-6">Product</div>
                    <div className="col-span-2 text-center">Quantity</div>
                    <div className="col-span-2 text-right">Unit Price</div>
                    <div className="col-span-2 text-right">Total</div>
                </div>

                {/* Einzelne Produkte */}
                {cartItems.map((item) => (
                    <div key={item.id} className="grid grid-cols-12 gap-4 items-center text-sm border-b py-3">
                        {/* Produktname + Bild */}
                        <div className="col-span-6 flex items-center gap-4">
                            <img
                                src={item.product.image}
                                alt={item.product.name}
                                className="w-16 h-16 object-cover rounded shadow"
                            />
                            <Link to={`/products/${item.product.id}`} className="hover:underline">
                                {item.product.name}
                            </Link>
                        </div>

                        {/* Menge */}
                        <div className="col-span-2 text-center">{item.quantity}</div>

                        {/* Einzelpreis */}
                        <div className="col-span-2 text-right">{item.product.price.toFixed(2)} €</div>

                        {/* Gesamtpreis */}
                        <div className="col-span-2 text-right font-medium">
                            {(item.quantity * item.product.price).toFixed(2)} €
                        </div>
                    </div>
                ))}

                {/* Zwischensumme */}
                <div className="flex justify-end font-semibold mt-4">
                    <div className="w-full max-w-sm flex justify-between border-t pt-4">
                        <span>Subtotal</span>
                        <span>{subtotal.toFixed(2)} €</span>
                    </div>
                </div>
            </section>
            <section className="mb-6">
                <h2 className="text-xl font-semibold mb-2">Invoice Address</h2>
                <div className="border p-3 rounded space-y-2">
                    <input type="text" placeholder="First Name" value={invoiceAddress.first_name}
                        onChange={(e) => setInvoiceAddress({ ...invoiceAddress, first_name: e.target.value })} className="w-full border px-2 py-1 rounded" />
                    <input type="text" placeholder="Last Name" value={invoiceAddress.last_name}
                        onChange={(e) => setInvoiceAddress({ ...invoiceAddress, last_name: e.target.value })} className="w-full border px-2 py-1 rounded" />
                    <input type="text" placeholder="Address" value={invoiceAddress.address}
                        onChange={(e) => setInvoiceAddress({ ...invoiceAddress, address: e.target.value })} className="w-full border px-2 py-1 rounded" />
                    <input type="text" placeholder="ZIP" value={invoiceAddress.post_code}
                        onChange={(e) => setInvoiceAddress({ ...invoiceAddress, post_code: e.target.value })} className="w-full border px-2 py-1 rounded" />
                    <input type="text" placeholder="City" value={invoiceAddress.city}
                        onChange={(e) => setInvoiceAddress({ ...invoiceAddress, city: e.target.value })} className="w-full border px-2 py-1 rounded" />
                    <select value={invoiceAddress.country}
                        onChange={(e) => setInvoiceAddress({ ...invoiceAddress, country: e.target.value })}
                        className="w-full px-3 py-2 border rounded">
                        <option value="">Select Country</option>
                        {countryList.map((c) => (
                            <option key={c.code} value={c.code}>{c.name}</option>
                        ))}
                    </select>
                </div>
            </section>
            <div className="mb-4">
                <label className="flex items-center gap-2">
                    <input
                        type="checkbox"
                        checked={showShippingFields}
                        onChange={(e) => setShowShippingFields(e.target.checked)}
                    />
                    Delivery address is different
                </label>
            </div>


            {showShippingFields && (
                <section className="mb-6">
                    <h2 className="text-xl font-semibold mb-2">Delivery Address</h2>
                    <div className="border p-3 rounded space-y-2">
                        <input type="text" placeholder="First Name" value={shippingAddress.first_name}
                            onChange={(e) => setShippingAddress({ ...shippingAddress, first_name: e.target.value })} className="w-full border px-2 py-1 rounded" />
                        <input type="text" placeholder="Last Name" value={shippingAddress.last_name}
                            onChange={(e) => setShippingAddress({ ...shippingAddress, last_name: e.target.value })} className="w-full border px-2 py-1 rounded" />
                        <input type="text" placeholder="Address" value={shippingAddress.address}
                            onChange={(e) => setShippingAddress({ ...shippingAddress, address: e.target.value })} className="w-full border px-2 py-1 rounded" />
                        <input type="text" placeholder="ZIP" value={shippingAddress.post_code}
                            onChange={(e) => setShippingAddress({ ...shippingAddress, post_code: e.target.value })} className="w-full border px-2 py-1 rounded" />
                        <input type="text" placeholder="City" value={shippingAddress.city}
                            onChange={(e) => setShippingAddress({ ...shippingAddress, city: e.target.value })} className="w-full border px-2 py-1 rounded" />
                        <select value={shippingAddress.country}
                            onChange={(e) => setShippingAddress({ ...shippingAddress, country: e.target.value })}
                            className="w-full px-3 py-2 border rounded">
                            <option value="">Select Country</option>
                            {countryList.map((c) => (
                                <option key={c.code} value={c.code}>{c.name}</option>
                            ))}
                        </select>
                    </div>
                </section>
            )}


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
                <h2 className="text-xl font-semibold mb-2">Payment Method</h2>
                <div className="space-y-2">
                    <label className="flex items-center gap-2">
                        <input
                            type="radio"
                            name="paymentMethod"
                            value="card"
                            checked={selectedPaymentMethod === "card"}
                            onChange={(e) => setSelectedPaymentMethod(e.target.value)}
                        />
                        Credit Card (Stripe)
                    </label>
                    <label className="flex items-center gap-2">
                        <input
                            type="radio"
                            name="paymentMethod"
                            value="klarna"
                            checked={selectedPaymentMethod === "klarna"}
                            onChange={(e) => setSelectedPaymentMethod(e.target.value)}
                        />
                        Klarna (Stripe)
                    </label>
                    <label className="flex items-center gap-2">
                        <input
                            type="radio"
                            name="paymentMethod"
                            value="paypal"
                            checked={selectedPaymentMethod === "paypal"}
                            onChange={(e) => setSelectedPaymentMethod(e.target.value)}
                        />
                        PayPal
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
                    I accept the <a href="/gtc" className="text-blue-600">GTC</a>
                </label>
            </section>
            {errorMessage && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                    <strong>Error:</strong> {errorMessage}
                </div>
            )}

            <button
                onClick={handlePayment}
                className="bg-black text-white px-6 py-3 rounded hover:bg-gray-800 disabled:opacity-50"
                disabled={!agreedToTerms || !selectedPaymentMethod}
            >
                pay now
            </button>
        </div>
    );
}

export default Checkout;
