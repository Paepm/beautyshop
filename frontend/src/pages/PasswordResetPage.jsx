import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Cookies from 'js-cookie';

import api from '../services/api';

function PasswordResetPage() {
    const { token } = useParams();
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();


    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (password !== confirmPassword) {
            setError('Passwords do not match.');
            return;
        }

        try {
            const response = await api.post(
                `accounts/password_reset/${token}/`,
                { password },
                {
                    headers: {
                        'X-CSRFToken': Cookies.get('csrftoken'),
                        'Content-Type': 'application/json',
                    },
                }
            );

            if (response.data.status === 'success') {
                setSuccess(true);
                setTimeout(() => { navigate('/login') }, 2000); // Redirect to login after 2 seconds
            } else {
                setError(response.data.message || 'Something went wrong.');
            }
        } catch (err) {
            setError(err.response?.data?.message || 'Server error occurred.');
        }
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-6 border rounded shadow">
            <h1 className="text-2xl font-semibold mb-4">Reset Password</h1>

            {success ? (
                <p className="text-green-700">
                    Password has been reset successfully. You can now log in.
                </p>
            ) : (
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium mb-1">New Password</label>
                        <input
                            type="password"
                            required
                            className="w-full border px-3 py-2 rounded"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Confirm Password</label>
                        <input
                            type="password"
                            required
                            className="w-full border px-3 py-2 rounded"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                        />
                    </div>

                    {error && <p className="text-red-600 text-sm">{error}</p>}

                    <button
                        type="submit"
                        className="bg-black text-white px-4 py-2 rounded hover:bg-gray-800"
                    >
                        Reset Password
                    </button>
                </form>
            )}
        </div>
    );
}

export default PasswordResetPage;
