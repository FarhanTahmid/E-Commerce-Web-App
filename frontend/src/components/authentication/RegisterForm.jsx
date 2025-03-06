import axios from 'axios';
import React, { useState } from 'react';
import { FiEye, FiEyeOff } from 'react-icons/fi';
import { Link, useNavigate } from 'react-router-dom';
import { BackendUrlMainAPI } from '../../BackendUrlMainAPI';

const RegisterForm = ({ path }) => {
    const [adminFullName, setAdminFullName] = useState('');
    const [adminEmail, setAdminEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [adminContactNo, setAdminContactNo] = useState('');
    const [adminAvatar, setAdminAvatar] = useState(null);

    const [error, setError] = useState(null);
    const [fieldErrors, setFieldErrors] = useState({});
    const [success, setSuccess] = useState(null);
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value, files } = e.target;

        if (name === 'admin_avatar') {
            setAdminAvatar(files ? files[0] : null);
        } else {
            switch (name) {
                case 'admin_full_name':
                    setAdminFullName(value);
                    break;
                case 'admin_email':
                    setAdminEmail(value);
                    break;
                case 'password':
                    setPassword(value);
                    break;
                case 'confirm_password':
                    setConfirmPassword(value);
                    break;
                case 'admin_contact_no':
                    setAdminContactNo(value);
                    break;
                default:
                    break;
            }
        }
    };

    const validateFields = () => {
        let errors = {};
        if (!adminFullName.trim()) errors.adminFullName = "Admin full name is required";
        if (!adminEmail.trim()) errors.adminEmail = "Admin email is required";
        if (!password) errors.password = "Password is required";
        if (!confirmPassword) errors.confirmPassword = "Confirm password is required";
        if (password !== confirmPassword) errors.confirmPassword = "Passwords do not match";

        setFieldErrors(errors);
        return Object.keys(errors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        if (!validateFields()) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('admin_full_name', adminFullName.trim());
        formData.append('admin_email', adminEmail.trim());
        formData.append('password', password);
        formData.append('confirm_password', confirmPassword);
        formData.append('admin_contact_no', adminContactNo.trim());

        if (adminAvatar) {
            formData.append('admin_avatar', adminAvatar);
        }

        try {
            const response = await axios.post(
                `${BackendUrlMainAPI}server_api/business-admin/signup/`,
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            );
            setLoading(false);
            setSuccess('Registration successful! Redirecting to login...');
            setTimeout(() => {
                navigate('/authentication/login');
            }, 2000);
        } catch (err) {
            setLoading(false);
            setError(err.response?.data?.error || 'An unexpected error occurred!');
        }
    };

    return (
        <>
            <h2 className="fs-20 fw-bolder mb-4">Register</h2>
            <h4 className="fs-13 fw-bold mb-2">Manage all your Duralux CRM</h4>
            <p className="fs-12 fw-medium text-muted">
                Let's get you all set up so you can verify your personal account and begin setting up your profile.
            </p>

            {error && (
                <div className="alert alert-danger alert-dismissible fade show" role="alert">
                    {error}
                    <button
                        type="button"
                        className="btn-close"
                        data-bs-dismiss="alert"
                        aria-label="Close"
                        onClick={() => setError(null)} // Close message on button click
                    ></button>
                </div>
            )}

            {success && (
                <div className="alert alert-success alert-dismissible fade show" role="alert">
                    {success}
                    <button
                        type="button"
                        className="btn-close"
                        data-bs-dismiss="alert"
                        aria-label="Close"
                        onClick={() => setSuccess(null)} // Close message on button click
                    ></button>
                </div>
            )}

            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Full Name</label>
                    <input type="text" name="admin_full_name" maxLength="50" value={adminFullName} onChange={handleChange} className="form-control" required />
                    {fieldErrors.adminFullName && <small className="text-danger">{fieldErrors.adminFullName}</small>}
                </div>

                <div className="form-group">
                    <label>Email</label>
                    <input type="email" name="admin_email" value={adminEmail} onChange={handleChange} className="form-control" required />
                    {fieldErrors.adminEmail && <small className="text-danger">{fieldErrors.adminEmail}</small>}
                </div>

                <div className="form-group">
                    <label>Contact Number</label>
                    <input type="text" name="admin_contact_no" value={adminContactNo} onChange={handleChange} className="form-control" required />
                </div>

                <div className="form-group">
                    <label>Password</label>
                    <div className="input-group">
                        <input type={showPassword ? "text" : "password"} name="password" value={password} onChange={handleChange} className="form-control" required />
                        <span className="input-group-text" onClick={() => setShowPassword(!showPassword)}>
                            {showPassword ? <FiEyeOff /> : <FiEye />}
                        </span>
                    </div>
                    {fieldErrors.password && <small className="text-danger">{fieldErrors.password}</small>}
                </div>

                <div className="form-group">
                    <label>Confirm Password</label>
                    <div className="input-group">
                        <input type={showConfirmPassword ? "text" : "password"} name="confirm_password" value={confirmPassword} onChange={handleChange} className="form-control" required />
                        <span className="input-group-text" onClick={() => setShowConfirmPassword(!showConfirmPassword)}>
                            {showConfirmPassword ? <FiEyeOff /> : <FiEye />}
                        </span>
                    </div>
                    {fieldErrors.confirmPassword && <small className="text-danger">{fieldErrors.confirmPassword}</small>}
                </div>

                <div className="form-group">
                    <label>Avatar</label>
                    <input type="file" name="admin_avatar" accept="image/png, image/jpg, image/jpeg" onChange={handleChange} className="form-control" required />
                </div>

                <button type="submit" className="btn btn-primary mt-3" disabled={loading}>
                    {loading ? "Registering..." : "Register"}
                </button>
            </form>

            <div className="mt-4 text-muted">
                <span>Already have an account?</span>
                <Link to={path} className="fw-bold"> Login</Link>
            </div>
        </>
    );
};

export default RegisterForm;
