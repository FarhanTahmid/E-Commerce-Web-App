import React, { useState, useEffect } from 'react';
import { FiEye, FiEyeOff, FiHash } from 'react-icons/fi';
import { Link, useNavigate } from 'react-router-dom';

const RegisterForm = ({ path }) => {
    const [formData, setFormData] = useState({
        admin_full_name: '',
        admin_email: '',
        password: '',
        confirm_password: '',
        admin_contact_no: '',
        admin_position_pk: '', // Now fetched from API
        admin_avatar: null, // File upload support
    });

    const [positions, setPositions] = useState([]); // Admin positions list
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const navigate = useNavigate();

    // Fetch admin positions on component mount
    useEffect(() => {
        const fetchPositions = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/business-admin/admin-position/fetch-positions/');
                const result = await response.json();
                if (response.ok) {
                    setPositions(result.positions); // Assuming API returns { positions: [{ id, name }] }
                } else {
                    throw new Error(result.error || "Failed to fetch positions.");
                }
            } catch (err) {
                setError(err.message);
            }
        };

        fetchPositions();
    }, []);

    const handleChange = (e) => {
        const { name, value, files } = e.target;
        setFormData({
            ...formData,
            [name]: files ? files[0] : value, // Handle file uploads
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        // Validate passwords match
        if (formData.password !== formData.confirm_password) {
            setError('Passwords do not match.');
            return;
        }

        // Prepare form data for submission
        const data = new FormData();
        for (const key in formData) {
            if (formData[key] !== null) {
                data.append(key, formData[key]);
            }
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/server_api/business-admin/signup/', {
                method: 'POST',
                body: data,
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Registration failed. Please try again.');
            }

            setSuccess('Registration successful! Redirecting to login...');
            setTimeout(() => {
                navigate(result.redirect_url || '/login-page');
            }, 2000); // Redirect after 2 seconds
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <>
            <h2 className="fs-20 fw-bolder mb-4">Register</h2>
            <h4 className="fs-13 fw-bold mb-2">Manage all your Duralux CRM</h4>
            <p className="fs-12 fw-medium text-muted">
                Let's get you all setup, so you can verify your personal account and begin setting up your profile.
            </p>
            {error && <div className="alert alert-danger">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}
            <form onSubmit={handleSubmit} className="w-100 mt-4 pt-2">
                <div className="mb-4">
                    <input
                        type="text"
                        className="form-control"
                        placeholder="Full Name"
                        name="admin_full_name"
                        value={formData.admin_full_name}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="mb-4">
                    <input
                        type="email"
                        className="form-control"
                        placeholder="Email"
                        name="admin_email"
                        value={formData.admin_email}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="mb-4">
                    <input
                        type="tel"
                        className="form-control"
                        placeholder="Contact Number"
                        name="admin_contact_no"
                        value={formData.admin_contact_no}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="mb-4">
                    <select
                        className="form-control"
                        name="admin_position_pk"
                        value={formData.admin_position_pk}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Select Admin Position</option>
                        {positions.map((position) => (
                            <option key={position.id} value={position.id}>
                                {position.name}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="mb-4 generate-pass">
                    <div className="input-group field">
                        <input
                            type={showPassword ? "text" : "password"}
                            className="form-control password"
                            placeholder="Password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                        />
                        <div
                            className="input-group-text c-pointer gen-pass"
                            data-bs-toggle="tooltip"
                            title="Generate Password"
                        >
                            <FiHash size={16} />
                        </div>
                        <div
                            className="input-group-text border-start bg-gray-2 c-pointer"
                            data-bs-toggle="tooltip"
                            title="Show/Hide Password"
                            onClick={() => setShowPassword(!showPassword)}
                        >
                            {showPassword ? <FiEyeOff size={16} /> : <FiEye size={16} />}
                        </div>
                    </div>
                </div>
                <div className="mb-4">
                    <div className="input-group field">
                        <input
                            type={showConfirmPassword ? "text" : "password"}
                            className="form-control"
                            placeholder="Confirm Password"
                            name="confirm_password"
                            value={formData.confirm_password}
                            onChange={handleChange}
                            required
                        />
                        <div
                            className="input-group-text border-start bg-gray-2 c-pointer"
                            data-bs-toggle="tooltip"
                            title="Show/Hide Password"
                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        >
                            {showConfirmPassword ? <FiEyeOff size={16} /> : <FiEye size={16} />}
                        </div>
                    </div>
                </div>
                <div className="mb-4">
                    <input
                        type="file"
                        className="form-control"
                        name="admin_avatar"
                        onChange={handleChange}
                    />
                </div>
                <div className="mt-4">
                    <div className="custom-control custom-checkbox mb-2">
                        <input type="checkbox" className="custom-control-input" id="receiveMail" required />
                        <label className="custom-control-label c-pointer text-muted" htmlFor="receiveMail">
                            Yes, I want to receive Duralux community emails
                        </label>
                    </div>
                    <div className="custom-control custom-checkbox">
                        <input type="checkbox" className="custom-control-input" id="termsCondition" required />
                        <label className="custom-control-label c-pointer text-muted" htmlFor="termsCondition">
                            I agree to all the <a href="#">Terms & Conditions</a> and <a href="#">Fees</a>.
                        </label>
                    </div>
                </div>
                <div className="mt-5">
                    <button type="submit" className="btn btn-lg btn-primary w-100">
                        Create Account
                    </button>
                </div>
            </form>
            <div className="mt-5 text-muted">
                <span>Already have an account?</span>
                <Link to={path} className="fw-bold"> Login</Link>
            </div>
        </>
    );
};

export default RegisterForm;
