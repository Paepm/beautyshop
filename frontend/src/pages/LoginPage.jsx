import React, { useState } from 'react';
import { fetchCSRFToken } from '../services/csrf';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

import { useAuth } from '../contexts/AuthContext';
import axios from '../services/api';


function LoginPage() {
    const [usernameOrEmail, setUsernameOrEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMsg, setErrorMsg] = useState('');
    const navigate = useNavigate();
    const { setIsAuthenticated } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            await fetchCSRFToken(); // get the CSRF token before making the login request

            const csrftoken = Cookies.get('csrftoken');

            await axios.post('/accounts/login/', {
                username_or_email: usernameOrEmail,
                password: password,
            }, {
                headers: {
                    'X-CSRFToken': csrftoken,
                },
            });

            setIsAuthenticated(true); // Update the authentication state to is authenticated
            navigate('/');
        } catch (error) {
            setErrorMsg('Login failed. Please check your credentials.');
        }
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
            <h2 className="text-2xl font-bold mb-4 text-center">Login</h2>
            {errorMsg && <p className="text-red-500 mb-3">{errorMsg}</p>}

            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label className="block font-semibold">Username or Email</label>
                    <input
                        type="text"
                        value={usernameOrEmail}
                        onChange={(e) => setUsernameOrEmail(e.target.value)}
                        required
                        className="w-full px-3 py-2 border rounded"
                    />
                </div>

                <div>
                    <label className="block font-semibold">Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="w-full px-3 py-2 border rounded"
                    />
                </div>

                <button
                    type="submit"
                    className="w-full bg-black text-white py-2 rounded hover:bg-gray-800 transition"
                >
                    Login
                </button>
            </form>
        </div>
    );
}

export default LoginPage;
