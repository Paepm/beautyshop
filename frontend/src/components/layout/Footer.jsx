import { Link } from 'react-router-dom';
import i18n from 'i18next';

import {baseUrl} from '../../services/api'; // Adjust the import path as necessary

function Footer() {
    return (
        <footer className="bg-yellow-100 border-b border-yellow-300 px-4 py-2">
            <div className="max-w-7xl mx-auto px-4 py-4 text-sm text-gray-600">
            {/* Linkliste – zentriert */}
                <div className="flex-1 flex justify-center flex-wrap gap-x-6 gap-y-2 text-center">
                    <Link to="/contact" className="hover:underline">
                        Contact Us
                    </Link>
                    <Link to="/privacy" className="hover:underline">
                        Data Protection
                    </Link>
                    <Link to="/gtc" className="hover:underline">
                        GTC
                    </Link>
                    <Link to="/imprint" className="hover:underline">
                        Imprint
                    </Link>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 py-4 text-sm text-gray-600">

                {/* Haupt-Layout: 3-Spalten-Ansatz */}
                <div className="flex flex-wrap justify-between items-start gap-y-4">

                    {/* Zahlungsarten – links */}
                    <div className="flex flex-col items-start text-xs text-gray-700 space-y-2">
                        <span className="font-semibold">Payment Methods</span>
                        <div className="flex flex-wrap gap-2 space-x-4">
                            <img src="/media/shop_page/paypal_logo.png" alt="PayPal" className="h-6" />
                            <img src="/media/shop_page/mastercard_logo.png" alt="Mastercard" className="h-6" />
                            <img src="/media/shop_page/visa_logo.png" alt="Visa" className="h-5" />
                            <img src="/media/shop_page/klarna_logo.png" alt="Klarna" className="h-6" />
                        </div>
                    </div>

                    {/* Sprachwahl – rechts */}
                    <div className="flex flex-col items-end text-xs text-gray-500">
                        <span className="font-semibold mb-1">Language:</span>
                        <div className="space-x-2">
                            <button onClick={() => i18n.changeLanguage('de')} title="Wechseln zu Deutsch">🇩🇪 DE</button>
                            <button onClick={() => i18n.changeLanguage('en')} title="Switch to English">🇬🇧 EN</button>
                        </div>
                    </div>
                </div>

                {/* Copyright */}
                <div className="text-xs text-gray-500 text-center mt-3">
                    &copy; {new Date().getFullYear()} WohnSinn – Your furniture world.
                </div>
            </div>
        </footer>
    );
}

export default Footer;
