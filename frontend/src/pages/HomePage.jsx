import { Link } from "react-router-dom";

function HomePage() {
    return (
        <div className="max-w-7xl mx-auto px-4 py-8 space-y-16">
            {/* Hero Section */}
            <section className="text-center space-y-6">
                <h1 className="text-4xl font-bold">Welcome to WohnSinnn</h1>
                <p className="text-lg text-gray-600 max-w-xl mx-auto">
                    Discover selected home accessories & furniture with style - perfect for your home.
                </p>
                <Link to="/productlist">
                    <button className="bg-black text-white px-6 py-3 rounded hover:bg-gray-800 transition-colors">
                        Discover products now
                    </button>
                </Link>
            </section>


            {/* USP / Trust Section */}
            <section className="bg-gray-100 p-8 rounded shadow text-center space-y-4">
                <h2 className="text-xl font-semibold">Why WohnSinnn?</h2>
                <ul className="grid grid-cols-1 md:grid-cols-3 gap-6 text-gray-700 text-sm">
                    <li>Hand-picked products with style</li>
                    <li>Fast & secure shipping</li>
                    <li>Personal support</li>
                </ul>
            </section>

            {/* Newsletter */}
            <section className="text-center space-y-4">
                <h2 className="text-xl font-semibold">Stay up to date</h2>
                <input
                    type="email"
                    placeholder="Your email address"
                    className="px-4 py-2 border rounded w-full max-w-xs"
                />
                <br />
                <button className="bg-black text-white px-6 py-2 rounded hover:bg-gray-800 transition">
                    Subscribe to our newsletter
                </button>
            </section>
        </div>
    );
}

export default HomePage;
