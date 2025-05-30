import { useState } from 'react';
import Cookies from 'js-cookie';

import api from '../services/api';

function LoosePwPage() {
    const [email, setEmail] = useState('');
    const [error, setError] = useState('');
    const [submitted, setSubmit] = useState(false);
    const csrfToken = Cookies.get('csrftoken');

    const handleSubmit = async (e) => {
        e.preventDefault();
        // setError('');
        try {
            await api.post('emails/password_reset/', { email }, {
                headers: {
                    'X-CSRFToken': csrfToken,
                    "Content-Type": "application/x-www-form-urlencoded"    // JSON is not supported by the backend, with that we can send the data as form-urlencoded
                },
            });
            setSubmit(true)
        }
        catch (err) {
            setError(
                err.response?.data?.email?.message ||
                'something went wrong, please try again later.'
            )
        }
    }

    return (
        <div className="max-w-md mx-auto mt-10 p-6 border rounded shadow">
            <h1 className="text-2xl font-semibold mb-4">Forgot Password</h1>

            {submitted ? (
                <p className="text-green-700">
                    If your email exists, a reset link has been sent.
                </p>
            ) : (
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium mb-1">Email address</label>
                        <input
                            type="email"
                            required
                            className="w-full border px-3 py-2 rounded"
                            placeholder="your@email.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                    </div>

                    {error && <p className="text-red-600 text-sm">{error}</p>}

                    <button
                        type="submit"
                        className="bg-black text-white px-4 py-2 rounded hover:bg-gray-800"
                    >
                        Send Reset Link
                    </button>
                </form>
            )}
        </div>
    );
}

export default LoosePwPage;
