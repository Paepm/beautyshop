// src/components/layout/Footer.jsx
import React from 'react';

function Footer() {
    return (
        <footer className="bg-gray-100 text-gray-600 text-center py-4 mt-8 shadow-inner">
            <div className="text-sm">
                &copy; {new Date().getFullYear()} Beautyshop by Patrick. All rights reserved.
            </div>
        </footer>
    );
}

export default Footer;
