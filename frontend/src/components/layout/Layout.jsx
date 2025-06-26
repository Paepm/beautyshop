import { Outlet, Link } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import FilterHeader from './FilterHeader';
import  {baseUrl} from '../../services/api'; // assuming you have a baseUrl defined

function Layout() {
    return (
        <div className="flex flex-col min-h-screen">
            {/* Fixierter Bereich oben */}
            <div className="fixed top-0 left-0 w-full z-50 bg-white shadow">
                <div className="relative max-w-7xl mx-auto">
                    {/* Logo über allem */}
                    <div className="absolute top-2 left-4 z-50">
                        <Link to="/">
                            <img
                                src="/media/shop_page/WohnsSinn_logo1.png"
                                alt="Logo"
                                className="h-20 hover:scale-110 transition-transform drop-shadow"
                            />
                        </Link>
                    </div>
                </div>
                <Header />
                <FilterHeader />
            </div>

            {/* Abstand unterhalb des fixierten Bereichs */}
            <div className="h-[96px]" /> {/* <- Höhe von Header + FilterHeader + Logo */}

            {/* Hauptinhalt */}
            <main className="flex-1 max-w-7xl mx-auto w-full px-4 py-8">
                <Outlet />
            </main>

            <Footer />
        </div>
    );
}

export default Layout;
