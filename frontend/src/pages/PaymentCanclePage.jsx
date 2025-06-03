// frontend/src/pages/CancelPage.jsx
import { Link } from "react-router-dom";

export default function CancelPage() {
    return (
        <div className="max-w-xl mx-auto mt-20 text-center">
            <h1 className="text-2xl font-bold text-red-600 mb-4">Zahlung abgebrochen</h1>
            <p className="mb-6 text-gray-700">
                Deine Zahlung wurde abgebrochen oder nicht abgeschlossen.
            </p>
            <div className="flex justify-center gap-4">
                <Link
                    to="/cart"
                    className="bg-gray-800 text-white px-4 py-2 rounded hover:bg-gray-700"
                >
                    Zurück zum Warenkorb
                </Link>
                <Link
                    to="/checkout"
                    className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-500"
                >
                    Erneut versuchen
                </Link>
            </div>
        </div>
    );
}
