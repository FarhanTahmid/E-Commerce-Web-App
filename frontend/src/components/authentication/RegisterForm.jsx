import axios from 'axios';
import React, { useState } from 'react';
import { FiEye, FiEyeOff } from 'react-icons/fi';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from "react-hook-form";


const RegisterForm = ({ path }) => {
    const [adminFullName, setAdminFullName] = useState('');
    const [adminEmail, setAdminEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [adminContactNo, setAdminContactNo] = useState('');

    // const [error, setError] = useState(null);
    const [fieldErrors, setFieldErrors] = useState({});
    const [success, setSuccess] = useState(null);
    // const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm();
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);
    const [error, setError] = useState(null);
    const [avatar, setAvatar] = useState(null);


    const onSubmit = async (data) => {
        setLoading(true);
        setSuccess(null);
        setError(null);

        const formData = new FormData();
        formData.append('admin_full_name', data.admin_full_name);
        formData.append('admin_email', data.admin_email);
        formData.append('password', data.password);
        formData.append('confirm_password', data.confirm_password);
        formData.append('admin_contact_no', data.admin_contact_no);
        if (avatar) {
            formData.append('admin_avatar', avatar);
        }

        // Log formData values
        for (let pair of formData.entries()) {
            console.log(pair[0] + ':', pair[1]); // This will log each key-value pair
        }

        try {
            const response = await axios.post('http://127.0.0.1:8000/server_api/business-admin/signup/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            alert(response.data.message);
        } catch (error) {
            alert(error.response?.data?.error || 'Something went wrong');
        }
        setLoading(false);
    };


    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
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

    // const handleSubmit = async (event) => {
    //     event.preventDefault();
    //     setError(null);
    //     setSuccess(null);

    //     if (!validateFields()) return;

    //     setLoading(true);

    //     const requestBody = {
    //         "admin_full_name": adminFullName,
    //         "admin_email": adminEmail,
    //         "password": password,
    //         "confirm_password": confirmPassword,
    //         "admin_contact_no": adminContactNo,
    //     };

    //     console.log('Request Body:', requestBody);


    //     try {
    //         const response = await axios.post(
    //             "http://127.0.0.1:8000/server_api/business-admin/signup/",
    //             requestBody,
    //             {
    //                 headers: {
    //                     "Content-Type": "application/json",
    //                 },
    //             }
    //         );

    //         console.log("Success:", response.data);
    //         setSuccess('Registration successful!');
    //         // Optionally, redirect after successful registration
    //         // navigate('/some-path');
    //     } catch (error) {
    //         if (error.response) {
    //             console.error("Server responded with an error:", error.response.data);
    //             setError(error.response?.data?.error || "An unexpected error occurred.");
    //         } else if (error.request) {
    //             console.error("Request was made but no response was received:", error.request);
    //             setError("No response from the server.");
    //         } else {
    //             console.error("Error setting up the request:", error.message);
    //             setError("An unexpected error occurred.");
    //         }
    //     }

    //     finally {
    //         setLoading(false);
    //     }
    // };

    return (
        <>
            <h2 className="fs-20 fw-bolder mb-4">Register</h2>
            <h4 className="fs-13 fw-bold mb-2">Manage all your Duralux CRM</h4>
            <p className="fs-12 fw-medium text-muted">
                Let's get you all setup, so you can verify your personal account and begin setting up your profile.
            </p>

            {error && <div className="alert alert-danger">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}

            <form onSubmit={handleSubmit(onSubmit)}>
                <div className="form-group">
                    <label>Full Name</label>
                    <input  {...register("admin_full_name", { required: "Full name is required" })} className="form-control" />
                    {errors.admin_full_name && <small className="text-danger">{errors.admin_full_name.message}</small>}
                </div>

                <div className="form-group">
                    <label>Email</label>
                    <input type="email" {...register("admin_email", { required: "Email is required" })} className="form-control" />
                    {errors.admin_email && <small className="text-danger">{errors.admin_email.message}</small>}
                </div>

                <div className="form-group">
                    <label>Contact Number</label>
                    <input {...register("admin_contact_no")} className="form-control" />
                </div>

                <div className="form-group">
                    <label>Password</label>
                    <div className="input-group">
                        <input type={showPassword ? "text" : "password"} {...register("password", { required: "Password is required" })} className="form-control" />
                        <span className="input-group-text" onClick={() => setShowPassword(!showPassword)}>
                            {showPassword ? <FiEyeOff /> : <FiEye />}
                        </span>
                    </div>
                    {errors.password && <small className="text-danger">{errors.password.message}</small>}
                </div>

                <div className="form-group">
                    <label>Confirm Password</label>
                    <div className="input-group">
                        <input type={showConfirmPassword ? "text" : "password"} {...register("confirm_password", { required: "Confirm password is required" })} className="form-control" />
                        <span className="input-group-text" onClick={() => setShowConfirmPassword(!showConfirmPassword)}>
                            {showConfirmPassword ? <FiEyeOff /> : <FiEye />}
                        </span>
                    </div>
                    {errors.confirm_password && <small className="text-danger">{errors.confirm_password.message}</small>}
                </div>

                <div className="form-group">
                    <label>Profile Picture</label>
                    <div className="input-group">
                        <input type="file" accept="image/*" onChange={(e) => setAvatar(e.target.files[0])} className="form-control" required />
                    </div>
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
