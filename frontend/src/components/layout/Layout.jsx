// src/components/layout/Layout.jsx
import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import FilterHeader from './FilterHeader';

function Layout() {
    return (
        <div className="flex flex-col min-h-screen">
            <Header />
            <FilterHeader />
            <main className="flex-1 max-w-7xl mx-auto w-full px-4 py-8">
                <Outlet />
            </main>

            <Footer />
        </div>
    );
}

export default Layout;
