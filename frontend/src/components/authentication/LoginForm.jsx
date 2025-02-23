import React, { useState } from 'react';
import { FiFacebook, FiGithub, FiTwitter } from 'react-icons/fi';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import { BackendUrlMainAPI } from '../../BackendUrlMainAPI';

const LoginForm = ({ registerPath, resetPath }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate(); // Initialize useNavigate

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await fetch(`${BackendUrlMainAPI}server_api/business-admin/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                // Assuming the API returns a token or success message
                // Set cookies with expiration times
                const accessTokenExpiry = new Date(new Date().getTime() + 2 * 24 * 60 * 60 * 1000); // 2 days
                const refreshTokenExpiry = new Date(new Date().getTime() + 2 * 24 * 60 * 60 * 1000); // 2 days

                Cookies.set('accessToken', data.access, { expires: accessTokenExpiry });
                Cookies.set('refreshToken', data.refresh, { expires: refreshTokenExpiry });
                Cookies.set('username', data.username, { expires: accessTokenExpiry }); // Optional: Set username cookie

                // Redirect to home page
                navigate('/', { replace: true }); // ✅ Corrected navigation
            } else {
                // Handle error response
                setError(data.error || 'Login failed. Please try again.');
            }
        } catch (err) {
            setError('An error occurred. Please try again later.');
        }
    };

    return (
        <>
            <h2 className="fs-20 fw-bolder mb-4">Login</h2>
            <h4 className="fs-13 fw-bold mb-2">Login to your account</h4>
            <p className="fs-12 fw-medium text-muted">Thank you for getting back to <strong>Nelel</strong> web applications. Let's access our best recommendations for you.</p>
            {error && <div className="alert alert-danger">{error}</div>}
            <form className="w-100 mt-4 pt-2" onSubmit={handleSubmit}>
                <div className="mb-4">
                    <input
                        type="text"
                        name="email"
                        className="form-control"
                        placeholder="Email Address"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="mb-3">
                    <input
                        type="password"
                        name="password"
                        className="form-control"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                {/* <div className="d-flex align-items-center justify-content-between">
                    <div>
                        <Link to={resetPath} className="fs-11 text-primary">Forget password?</Link>
                    </div>
                </div> */}
                <div className="mt-5">
                    <button type="submit" className="btn btn-lg btn-primary w-100">Login</button>
                </div>
            </form>
            <div className="mt-5 text-muted">
                <span> Don't have an account?</span>
                <Link to={registerPath} className="fw-bold"> Create an Account</Link>
            </div>
        </>
    );
};

export default LoginForm;
