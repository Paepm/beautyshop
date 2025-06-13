const GTCPage = () => {
    return (
        <div className="max-w-4xl mx-auto px-4 py-8 text-sm leading-relaxed space-y-4">
            <h1 className="text-2xl font-bold mb-6">General Terms and Conditions (GTC)</h1>

            <p>
                These General Terms and Conditions (hereinafter "GTC") apply to all orders placed via our online shop WohnSinn
                (hereinafter "we", "us") accessible at www.wohnsinn.at. The terms define the conditions for using the online shop and
                concluding purchase contracts with us. By placing an order, you agree to these GTC.
            </p>

            <h2 className="text-lg font-semibold mt-6">1. Scope and Contract Partner</h2>
            <p>
                These GTC apply to all purchases by consumers and businesses via our online shop. Our customers are both private
                individuals and companies. The contract is concluded with WohnSinn, operated by:
                <br />
                <strong>WohnSinn e.U., Sample Street 1, 1234 Sampletown, Austria</strong>
            </p>

            <h2 className="text-lg font-semibold mt-6">2. Order Process and Contract Conclusion</h2>
            <p>
                The presentation of products in our shop is not a legally binding offer, but a non-binding catalog. You submit a
                binding offer by completing the checkout process and clicking the “Buy now” button. A binding contract is only
                concluded once you receive an order confirmation by email.
            </p>

            <h2 className="text-lg font-semibold mt-6">3. Prices and Payment</h2>
            <p>
                All prices include applicable VAT and exclude shipping costs. The final total price including shipping will be shown
                during checkout. Payment methods include PayPal, credit card (via Stripe), Klarna, and Apple Pay. Payment is due
                immediately upon order placement.
            </p>

            <h2 className="text-lg font-semibold mt-6">4. Shipping and Delivery</h2>
            <p>
                Delivery is made within Austria, Germany, Liechtenstein, and Switzerland unless otherwise agreed. Delivery times
                depend on the availability of the products and are indicated on the product pages. We reserve the right to partial
                deliveries at no additional cost to the customer.
            </p>

            <h2 className="text-lg font-semibold mt-6">5. Right of Withdrawal</h2>
            <p>
                As a consumer, you have the right to withdraw from your purchase within 14 days without giving a reason. The withdrawal
                period begins from the day the goods are received. To exercise the right of withdrawal, send us a clear declaration via
                email. We will refund all payments including shipping costs within 14 days using the original payment method.
            </p>

            <h2 className="text-lg font-semibold mt-6">6. Retention of Title</h2>
            <p>
                The goods remain our property until full payment is received.
            </p>

            <h2 className="text-lg font-semibold mt-6">7. Warranty and Liability</h2>
            <p>
                The statutory warranty laws apply. We are only liable for damages caused intentionally or by gross negligence. Liability
                for slight negligence is excluded unless it concerns the breach of essential contractual obligations (cardinal duties).
            </p>

            <h2 className="text-lg font-semibold mt-6">8. Dispute Resolution</h2>
            <p>
                The EU Commission provides an online dispute resolution platform at <a href="https://ec.europa.eu/consumers/odr" className="text-blue-600 underline" target="_blank" rel="noreferrer">https://ec.europa.eu/consumers/odr</a>. We are not
                obliged or willing to participate in dispute resolution proceedings before a consumer arbitration board.
            </p>

            <h2 className="text-lg font-semibold mt-6">9. Final Provisions</h2>
            <p>
                Austrian law applies, excluding the UN Convention on Contracts for the International Sale of Goods (CISG). If any
                provision of these GTC is invalid, the remaining provisions remain unaffected.
            </p>

            <p>Last updated: June 2025</p>
        </div>
    );
};

export default GTCPage;
