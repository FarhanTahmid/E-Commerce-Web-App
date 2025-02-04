import React, { useState } from 'react';
import { FiEye, FiEyeOff } from 'react-icons/fi';
import { Link, useNavigate } from 'react-router-dom';

const RegisterForm = ({ path }) => {
    const [formData, setFormData] = useState({
        admin_full_name: '',
        admin_email: '',
        password: '',
        confirm_password: '',
        admin_contact_no: '',
        admin_avatar: null,
    });
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value, files } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: files ? files[0] : value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        if (formData.password !== formData.confirm_password) {
            setError('Passwords do not match.');
            return;
        }

        const data = new FormData();
        for (const key in formData) {
            if (formData[key] !== null) {
                data.append(key, formData[key]);
            }
        }

        // Log FormData values before sending
        for (let pair of data.entries()) {
            console.log(pair[0] + ':', pair[1]);
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/server_api/business-admin/signup/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData),
            });


            const result = await response.json();
            console.log("Server Response:", result); // Log response

            if (!response.ok) {
                console.error("Full Error Response:", result);
                throw new Error(result.message || 'An unexpected error occurred while creating admin user! Please try again later.');
            }

            setSuccess('Registration successful! Redirecting to login...');
            setTimeout(() => {
                navigate('/authentication/login/minimal');
            }, 2000);
        } catch (err) {
            setError(err.message);
            console.error("Error:", err.message);
        }
    };


    return (
        <>
            <h2 className="fs-20 fw-bolder mb-4">Register</h2>
            <h4 className="fs-13 fw-bold mb-2">Manage all your Duralux CRM</h4>
            <p className="fs-12 fw-medium text-muted">
                Let's get you all setup, so you can verify your personal account and begin setting up your profile.
            </p>

            {error && (
                <div className="alert alert-danger alert-dismissible fade show" role="alert">
                    {error}
                    <button type="button" className="btn-close" onClick={() => setError(null)}></button>
                </div>
            )}
            {success && (
                <div className="alert alert-success alert-dismissible fade show" role="alert">
                    {success}
                    <button type="button" className="btn-close" onClick={() => setSuccess(null)}></button>
                </div>
            )}

            <form onSubmit={handleSubmit} className="w-100 mt-4 pt-2">
                <input type="text" className="form-control mb-3" placeholder="Full Name" name="admin_full_name" value={formData.admin_full_name} onChange={handleChange} required />
                <input type="email" className="form-control mb-3" placeholder="Email" name="admin_email" value={formData.admin_email} onChange={handleChange} required />
                <input type="tel" className="form-control mb-3" placeholder="Contact Number" name="admin_contact_no" value={formData.admin_contact_no} onChange={handleChange} required />

                <div className="mb-3 input-group">
                    <input type={showPassword ? "text" : "password"} className="form-control" placeholder="Password" name="password" value={formData.password} onChange={handleChange} required />
                    <button className="input-group-text" type="button" onClick={() => setShowPassword(!showPassword)}>
                        {showPassword ? <FiEyeOff size={16} /> : <FiEye size={16} />}
                    </button>
                </div>
                <div className="mb-3 input-group">
                    <input type={showConfirmPassword ? "text" : "password"} className="form-control" placeholder="Confirm Password" name="confirm_password" value={formData.confirm_password} onChange={handleChange} required />
                    <button className="input-group-text" type="button" onClick={() => setShowConfirmPassword(!showConfirmPassword)}>
                        {showConfirmPassword ? <FiEyeOff size={16} /> : <FiEye size={16} />}
                    </button>
                </div>
                <input type="file" className="form-control mb-3" name="admin_avatar" onChange={handleChange} />

                <div className="form-check mb-2">
                    <input type="checkbox" className="form-check-input" id="receiveMail" required />
                    <label className="form-check-label" htmlFor="receiveMail">
                        Yes, I want to receive Duralux community emails
                    </label>
                </div>
                <div className="form-check mb-4">
                    <input type="checkbox" className="form-check-input" id="termsCondition" required />
                    <label className="form-check-label" htmlFor="termsCondition">
                        I agree to all the <a href="#">Terms & Conditions</a> and <a href="#">Fees</a>.
                    </label>
                </div>

                <button type="submit" className="btn btn-lg btn-primary w-100">Create Account</button>
            </form>

            <div className="mt-4 text-muted">
                <span>Already have an account?</span>
                <Link to={path} className="fw-bold"> Login</Link>
            </div>
        </>
    );
};

export default RegisterForm;