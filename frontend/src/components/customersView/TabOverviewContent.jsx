import React, { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import { set } from 'date-fns';


const TabOverviewContent = () => {
    const [userInfo, setUserInfo] = useState(null);
    const [position, setPosition] = useState('');
    const [isEditing, setIsEditing] = useState(false);
    const [message, setMessage] = useState('');
    const [messageType, setMessageType] = useState(''); // 'success' or 'error'

    const username = Cookies.get('username');
    const API_BASE_URL = 'http://127.0.0.1:8000/server_api/business-admin/';

    useEffect(() => {
        fetchUserInfo();
    }, []);

    useEffect(() => {
        if (userInfo && userInfo.admin_position) {
            fetchPosition(userInfo.admin_position);
        }
    }, [userInfo]);  // This runs whenever userInfo changes

    const fetchUserInfo = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}admin/fetch-all/?admin_user_name=${username}`, {
                headers: {
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                },
            });

            const data = await response.json();

            if (data.admin_users) {
                setUserInfo(data.admin_users);  // Triggers useEffect to fetch position
            }
        } catch (error) {
            console.error('Error fetching user info:', error);
        }
    };

    const fetchPosition = async (adminPositionId) => {
        try {
            const response = await fetch(`${API_BASE_URL}admin-position/fetch-positions/`, {
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                }
            });

            const data = await response.json();

            if (data.admin_positions && Array.isArray(data.admin_positions)) {
                const positionData = data.admin_positions.find(pos => pos.id === adminPositionId);
                if (positionData) {
                    setPosition(positionData.name);
                } else {
                    console.warn("Position not found for admin_position:", adminPositionId);
                }
            }
        } catch (error) {
            console.error('Error fetching position:', error);
        }
    };

    const formatDate = (dateString) => {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setUserInfo(prevState => ({
            ...prevState,
            [name]: value
        }));
    };
    const handleSave = async () => {
        if (!userInfo.admin_full_name || !userInfo.admin_email || !userInfo.admin_contact_no) {
            setMessage('All fields are required.');
            setMessageType('error');
            return;
        }
        const updatedFormData = {
            admin_full_name: userInfo.admin_full_name,
            admin_email: userInfo.admin_email,
            admin_contact_no: userInfo.admin_contact_no,
        };

        try {
            const response = await fetch(`${API_BASE_URL}update/${userInfo.admin_user_name}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${Cookies.get("accessToken")}`,
                },
                body: JSON.stringify(updatedFormData)
            });

            const responseData = await response.json();

            if (response.ok) {
                setUserInfo({ ...userInfo, ...updatedFormData });
                setIsEditing(false);
                setMessage('Profile updated successfully!');
                setMessageType('success');
                window.location.reload();
            } else {
                setMessage(responseData.error || 'Failed to update profile.');
                setMessageType('error');
            }
        } catch (error) {
            setMessage('Error updating profile. Please try again.');
            setMessageType('error');
        }
    };

    const closeMessage = () => {
        setMessage('');
        setMessageType('');
    };

    if (!userInfo) return <p>Loading...</p>;

    return (
        <div className="tab-pane fade show active p-4" id="overviewTab" role="tabpanel">
            {message && (
                <div className={`alert alert-${messageType === 'success' ? 'success' : 'danger'} alert-dismissible fade show`} role="alert">
                    {message}
                    <button type="button" className="btn-close" onClick={closeMessage}></button>
                </div>
            )}
            <div className="profile-details mb-5">
                <div className="mb-4 d-flex align-items-center justify-content-between">
                    <h5 className="fw-bold mb-0">Profile Details:</h5>
                    <button className="btn btn-sm btn-light-brand" onClick={() => setIsEditing(!isEditing)}>
                        {isEditing ? 'Cancel' : 'Edit Profile'}
                    </button>
                </div>
                <div className="row g-0 mb-4">
                    <div className="col-sm-6 text-muted">Full Name:</div>
                    <div className="col-sm-6 fw-semibold">
                        {isEditing ? (
                            <input
                                className='form-label'
                                name="admin_full_name"
                                value={userInfo.admin_full_name}
                                onChange={handleInputChange}
                            />
                        ) : (
                            userInfo.admin_full_name
                        )}
                    </div>
                </div>
                <div className="row g-0 mb-4">
                    <div className="col-sm-6 text-muted">Username:</div>
                    <div className="col-sm-6 fw-semibold">{userInfo.admin_user_name}</div>
                </div>
                <div className="row g-0 mb-4">
                    <div className="col-sm-6 text-muted">Position:</div>
                    <div className="col-sm-6 fw-semibold">{position || "Not Assigned"}</div>
                </div>
                <div className="row g-0 mb-4">
                    <div className="col-sm-6 text-muted">Email Address:</div>
                    <div className="col-sm-6 fw-semibold">
                        {isEditing ? (
                            <input
                                className='form-label'
                                name="admin_email"
                                value={userInfo.admin_email}
                                onChange={handleInputChange}
                            />
                        ) : (
                            userInfo.admin_email
                        )}
                    </div>
                </div>
                <div className="row g-0 mb-4">
                    <div className="col-sm-6 text-muted">Contact No:</div>
                    <div className="col-sm-6 fw-semibold">
                        {isEditing ? (
                            <input
                                className='form-label'
                                name="admin_contact_no"
                                value={userInfo.admin_contact_no}
                                onChange={handleInputChange}
                            />
                        ) : (
                            userInfo.admin_contact_no
                        )}
                    </div>
                </div>
                <div className="row g-0 mb-4">
                    <div className="col-sm-6 text-muted">Joining Date:</div>
                    <div className="col-sm-6 fw-semibold">{formatDate(userInfo.admin_account_created_at)}</div>
                </div>
                {isEditing && <button className="btn btn-primary" onClick={handleSave}>Save</button>}
            </div>
        </div>
    );
};

export default TabOverviewContent;