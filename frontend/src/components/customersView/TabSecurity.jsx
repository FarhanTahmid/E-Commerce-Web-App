import Cookies from 'js-cookie';
import React, { useState } from 'react'
import { FiEye, FiEyeOff } from 'react-icons/fi';
import { useNavigate } from 'react-router-dom';

const TabSecurity = () => {
    const navigate = useNavigate();
    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'error'

    const [showOldPassword, setShowOldPassword] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/business-admin/';

    const userName = Cookies.get('username');

    const closeMessage = () => {
        setMessage('');
        setMessageType('');
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (newPassword !== confirmPassword) {
            setMessage('Passwords do not match');
            setMessageType('error');
            return;
        }
        try {
            const response = await fetch(`${API_BASE_URL}update-password/${userName}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                },
                body: JSON.stringify({
                    old_password: currentPassword,
                    new_password: newPassword,
                    new_password_confirm: confirmPassword,
                }),
            });
            if (!response.ok) {
                setMessage('Error changing password. Please try again later.');
                setMessageType('error');
                return;
            }
            setCurrentPassword('');
            setNewPassword('');
            setConfirmPassword('');
            setMessage('Password changed successfully');
            setMessageType('success');
        } catch (error) {
            setMessage('Error changing password. Please try again later.');
            setMessageType('error');
            console.error('Error changing password:', error);
        }
    }

    const handleSubmitDeletion = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${API_BASE_URL}delete/${userName}/`, {
                method: 'DELETE',
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                },
            });
            if (!response.ok) {
                setMessage('Error deleting account. Please try again later.');
                setMessageType('error');
                return;
            }
            setMessage('Account deleted successfully');
            setMessageType('success');
            Cookies.remove('accessToken');
            Cookies.remove('username');
            Cookies.remove('refreshToken');
            navigate('/authentication/login/minimal');
        } catch (error) {
            setMessage('Error deleting account. Please try again later.');
            setMessageType('error');
            console.error('Error deleting account:', error);
        }
    }

    return (
        <div className="tab-pane fade p-4" id="securityTab" role="tabpanel">
            {/* <SecurityFeature
                title="Two-factor Authentication"
                description="Two-factor authentication is an enhanced security measure. Once enabled, you'll be required to give two types of identification when you log into Google Authentication and SMS are Supported."
                label="Enable 2FA Verification"
                checkboxId="2faVerification"
                isChecked={true}
            />
            <SecurityFeature
                title="Secondary Verification"
                description="The first factor is a password and the second commonly includes a text with a code sent to your smartphone, or biometrics using your fingerprint, face, or retina."
                label="Set up secondary method"
                checkboxId="secondaryVerification"
                isChecked={true}
            />
            <SecurityFeature
                title="Backup Codes"
                description="A backup code is automatically generated for you when you turn on two-factor authentication through your iOS or Android Twitter app. You can also generate a backup code on twitter.com."
                label="Generate backup codes"
                checkboxId="generateBackup"
                isChecked={false}
            />
            <SecurityFeature
                title="Login Verification"
                description="Login verification is an enhanced security measure. Once enabled, you'll be required to give two types of identification when you log into Google Authentication and SMS are Supported."
                label="Enable Login Verification"
                checkboxId="loginVerification"
                isChecked={true}
            /> */}
            {message && (
                <div className={`alert alert-${messageType === 'success' ? 'success' : 'danger'} alert-dismissible fade show`} role="alert">
                    {message}
                    <button type="button" className="btn-close" onClick={closeMessage}></button>
                </div>
            )}
            <form className="mt-4" onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label htmlFor="currentPassword" className="form-label">Current Password</label>
                    <div className="input-group">
                        <input type={showOldPassword ? "text" : "password"} className="form-control" id="currentPassword" placeholder="Enter your current password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} required />
                        <span className="input-group-text" onClick={() => setShowOldPassword(!showOldPassword)}>
                            {showOldPassword ? <FiEyeOff /> : <FiEye />}
                        </span>
                    </div>
                </div>
                <div className="mb-4">
                    <label htmlFor="newPassword" className="form-label">New Password</label>
                    <div className="input-group">
                        <input type={showPassword ? "text" : "password"} className="form-control" id="newPassword" placeholder="Enter your new password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
                        <span className="input-group-text" onClick={() => setShowPassword(!showPassword)}>
                            {showPassword ? <FiEyeOff /> : <FiEye />}
                        </span>
                    </div>
                </div>
                <div className="mb-4">
                    <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
                    <div className="input-group">
                        <input type={showConfirmPassword ? "text" : "password"} className="form-control" id="confirmPassword" placeholder="Confirm your new password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
                        <span className="input-group-text" onClick={() => setShowConfirmPassword(!showConfirmPassword)}>
                            {showConfirmPassword ? <FiEyeOff /> : <FiEye />}
                        </span>
                    </div>
                </div>
                <button type="submit" className="btn btn-primary">Change Password</button>
            </form>
            <hr className="my-5" />
            <div className="alert alert-dismissible mb-4 p-4 d-flex alert-soft-danger-message" role="alert">
                <div className="me-4 d-none d-md-block">
                    <i className="feather feather-alert-triangle text-danger fs-1"></i>
                </div>
                <div>
                    <p className="fw-bold mb-0 text-truncate-1-line">You Are Deleting Your Account</p>
                    <p className="text-truncate-3-line mt-2 mb-4">Once you delete your account, there is no going back. Please be certain.</p>
                    <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            </div>
            <div className="card mt-5">
                <div className="card-body">
                    <h6 className="fw-bold">Delete Account</h6>
                    <p className="fs-11 text-muted">Once you delete your account, there is no going back. Please be certain.</p>
                    <form className="mt-4" onSubmit={handleSubmitDeletion}>

                        <div className="my-4 py-2">
                            <div className="mt-3">
                                <div className="custom-control custom-checkbox">
                                    <input type="checkbox" className="custom-control-input" id="acDeleteDeactive" required />
                                    <label className="custom-control-label c-pointer" htmlFor="acDeleteDeactive">I confirm my account deletation.</label>
                                </div>
                            </div>
                        </div>
                        <div className="d-sm-flex gap-2">
                            <button type="submit" className="btn btn-danger">Delete Account</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default TabSecurity


const SecurityFeature = ({ title, description, label, checkboxId, isChecked }) => {
    return (
        <div className="p-4 mb-4 border border-dashed border-gray-3 rounded-1">
            <h6 className="fw-bolder"><a href="#">{title}</a></h6>
            <div className="fs-12 text-muted text-truncate-3-line mt-2 mb-4">{description}</div>
            <div className="form-check form-switch form-switch-sm">
                <label className="form-check-label fw-500 text-dark c-pointer" htmlFor={checkboxId}>{label}</label>
                <input className="form-check-input c-pointer" type="checkbox" id={checkboxId} defaultChecked={isChecked} />
            </div>
        </div>
    );
};