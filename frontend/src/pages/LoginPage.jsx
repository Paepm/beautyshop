import { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';

import { AuthContext } from '../contexts/AuthContext';
import { loginUser } from '../services/auth';


function LoginPage() {
    const [usernameOrEmail, setUsernameOrEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMsg, setErrorMsg] = useState('');
    const navigate = useNavigate();
    const { setIsAuthenticated, refreshAuth } = useContext(AuthContext);
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            await loginUser(usernameOrEmail, password); // Call the loginUser function to perform the login
            await refreshAuth(); // Refresh the authentication state after login, is needed to get user from AuthContext in ProfileDropdown
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

                <Link to="/password_reset">
                    Forgot your password? Click Here!
                </Link>
            </form>
        </div>
    );
}

export default LoginPage;
