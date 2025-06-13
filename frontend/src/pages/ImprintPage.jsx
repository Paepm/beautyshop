const ImprintPage = () => {
    return (
        <div className="max-w-3xl mx-auto px-4 py-8 text-sm leading-relaxed space-y-4">
            <h1 className="text-2xl font-bold mb-6">Imprint</h1>

            <p>
                <strong>WohnSinn e.U.</strong><br />
                Max-Mustermann-Straße 1<br />
                1010 Wien<br />
                Austria
            </p>

            <p>
                Phone: +43 123 456789<br />
                E-Mail: office@wohnsinn.at<br />
                Website: www.wohnsinn.at
            </p>

            <p>
                Owner: Max Mustermann<br />
                Company form: Einzelunternehmen (e.U.)<br />
                Commercial Register No.: FN 123456a<br />
                Commercial Court: Handelsgericht Wien<br />
                VAT ID: ATU12345678
            </p>

            <p>
                Responsible for content according to § 55 Abs. 2 RStV: Max Mustermann
            </p>

            <p>
                <strong>Online Dispute Resolution (OS)</strong><br />
                The European Commission provides a platform for online dispute resolution (ODR):<br />
                <a
                    href="https://ec.europa.eu/consumers/odr"
                    className="text-blue-600 underline"
                    target="_blank"
                    rel="noreferrer"
                >
                    https://ec.europa.eu/consumers/odr
                </a>
            </p>

            <p>
                We are not willing or obliged to participate in dispute resolution proceedings before a consumer arbitration board.
            </p>

            <p className="text-gray-500 mt-8">Last updated: June 2025</p>
        </div>
    );
};

export default ImprintPage;
