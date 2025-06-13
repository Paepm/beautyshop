const PrivacyPage = () => {
    return (
        <div className="max-w-3xl mx-auto px-4 py-8 text-sm leading-relaxed space-y-4">
            <h1 className="text-2xl font-bold mb-6">Privacy Policy</h1>

            <p>
                We take the protection of your personal data very seriously. This Privacy Policy informs you about how we collect, use, and protect your information when you visit our website or use our services.
            </p>

            <h2 className="text-lg font-semibold mt-6">1. Data Controller</h2>
            <p>
                WohnSinn e.U.<br />
                Max-Mustermann-Straße 1<br />
                1010 Vienna, Austria<br />
                Email: privacy@wohnsinn.at
            </p>

            <h2 className="text-lg font-semibold mt-6">2. What Data We Collect</h2>
            <p>
                We may collect and process the following types of personal data:
            </p>
            <ul className="list-disc list-inside">
                <li>Contact information (name, email, address)</li>
                <li>Account details (username, login data)</li>
                <li>Order and payment information</li>
                <li>Device and browser information</li>
                <li>IP address and usage data</li>
            </ul>

            <h2 className="text-lg font-semibold mt-6">3. Purpose of Data Processing</h2>
            <p>
                Your data is processed for the following purposes:
            </p>
            <ul className="list-disc list-inside">
                <li>To provide and improve our services</li>
                <li>To process orders and payments</li>
                <li>To provide customer support</li>
                <li>To comply with legal obligations</li>
                <li>To send order confirmations and updates</li>
            </ul>

            <h2 className="text-lg font-semibold mt-6">4. Legal Basis</h2>
            <p>
                We process your data based on your consent, the necessity to fulfill a contract, legal obligations, or our legitimate interest in improving our services.
            </p>

            <h2 className="text-lg font-semibold mt-6">5. Cookies and Tracking</h2>
            <p>
                We use cookies to enhance user experience and analyze traffic. You can adjust your cookie preferences at any time in your browser settings.
            </p>

            <h2 className="text-lg font-semibold mt-6">6. Data Sharing</h2>
            <p>
                We only share your data with third parties when necessary for order processing (e.g. payment providers, shipping companies) or when legally required.
            </p>

            <h2 className="text-lg font-semibold mt-6">7. Your Rights</h2>
            <p>
                You have the right to access, correct, delete, or restrict the use of your personal data. Please contact us at <strong>privacy@wohnsinn.at</strong> to exercise your rights.
            </p>

            <h2 className="text-lg font-semibold mt-6">8. Data Storage</h2>
            <p>
                We store your data only as long as necessary to fulfill the purposes outlined in this policy or as required by law.
            </p>

            <h2 className="text-lg font-semibold mt-6">9. Contact</h2>
            <p>
                If you have questions about our privacy practices, feel free to reach out to: <br />
                <strong>Email:</strong> privacy@wohnsinn.at
            </p>

            <p className="text-gray-500 mt-8">Last updated: June 2025</p>
        </div>
    );
};

export default PrivacyPage;
