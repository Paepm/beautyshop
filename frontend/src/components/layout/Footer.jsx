import React from 'react';
import { Link } from 'react-router-dom';

function Footer() {
    return (
        <footer className="bg-yellow-100 border-b border-yellow-300 px-4 py-2">
            <div className="max-w-7xl mx-auto px-4 py-4 flex flex-col items-center text-sm text-gray-600">

                {/* Linkliste – immer zentriert */}
                <div className="flex flex-wrap justify-center gap-x-6 gap-y-2 text-center mb-2">
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

                {/* Copyright */}
                <div className="text-xs text-gray-500 text-center">
                    &copy; {new Date().getFullYear()} WohnSinnn – Your furniture world.
                </div>
            </div>
        </footer>
    );
}

export default Footer;
